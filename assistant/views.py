import requests
from django.conf import settings
from pgvector.django import CosineDistance
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Document, DocumentChunk
from .serializers import DocumentSerializer, DocumentCreateSerializer, AskQuestionSerializer
from .chunking import chunk_text
from .embeddings import generate_embeddings_batch


@api_view(["GET", "POST"])
def document_list(request):
    """List all documents or upload a new one."""
    if request.method == "GET":
        documents = Document.objects.all().order_by("-created_at")
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

    serializer = DocumentCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    doc = serializer.save()

    chunks = chunk_text(doc.content)

    if not chunks:
        return Response(DocumentSerializer(doc).data, status=status.HTTP_201_CREATED)

    embeddings = generate_embeddings_batch(chunks)

    chunk_objects = [
        DocumentChunk(
            document=doc,
            chunk_text=text,
            chunk_index=idx,
            embedding=emb,
        )
        for idx, (text, emb) in enumerate(zip(chunks, embeddings))
    ]
    DocumentChunk.objects.bulk_create(chunk_objects)

    return Response(DocumentSerializer(doc).data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def ask_question(request):
    """Embed the question, retrieve top-5 relevant chunks, and generate a grounded answer."""
    serializer = AskQuestionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    question = serializer.validated_data["question"]

    question_embedding = generate_embeddings_batch([question])[0]

    results = (
        DocumentChunk.objects.annotate(
            distance=CosineDistance("embedding", question_embedding)
        )
        .select_related("document")
        .order_by("distance")[:5]
    )

    if not results:
        return Response(
            {"answer": "No documents have been ingested yet.", "sources": []},
            status=status.HTTP_200_OK,
        )

    context = "\n\n".join(
        f"[{chunk.document.title}]\n{chunk.chunk_text}" for chunk in results
    )

    system_prompt = (
        "You are a study assistant. Answer the user's question using ONLY the "
        "information in the <context> below. If the context does not contain "
        "enough information to answer the question, say so explicitly — do not "
        "make up or infer information that isn't present in the context.\n\n"
        f"<context>\n{context}\n</context>"
    )

    llm_response = requests.post(
        f"{settings.LLM_API_BASE_URL}/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.LLM_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": settings.LLM_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            "temperature": 0.3,
        },
        timeout=60,
    )
    llm_response.raise_for_status()
    answer = llm_response.json()["choices"][0]["message"]["content"]

    sources = [
        {
            "title": chunk.document.title,
            "preview": chunk.chunk_text[:200],
            "relevance_score": round(1 - chunk.distance, 4),
        }
        for chunk in results
    ]

    return Response({"answer": answer, "sources": sources})