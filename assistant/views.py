from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Document, DocumentChunk, Conversation
from .serializers import DocumentSerializer, DocumentCreateSerializer, AskQuestionSerializer, ConversationSerializer, ConversationCreateSerializer
from .chunking import chunk_text
from .embeddings import generate_embeddings_batch
from .rag import retrieve_relevant_chunks, generate_rag_response, ask_with_rag


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
    """One-off RAG answer, no conversation history."""
    serializer = AskQuestionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    question = serializer.validated_data["question"]

    chunks = retrieve_relevant_chunks(question, top_k=5)

    if not chunks:
        return Response(
            {"answer": "No documents have been ingested yet.", "sources": []},
            status=status.HTTP_200_OK,
        )

    answer = generate_rag_response(question, chunks)

    sources = [
        {
            "title": chunk["document_title"],
            "preview": chunk["chunk_text"][:200],
            "relevance_score": round(1 - chunk["distance"], 4),
        }
        for chunk in chunks
    ]

    return Response({"answer": answer, "sources": sources})


@api_view(["POST"])
def conversation_create(request):
    """Start a new conversation."""
    serializer = ConversationCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    conversation = serializer.save()
    return Response(
        ConversationSerializer(conversation).data,
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
def conversation_detail(request, conversation_id):
    """Get a conversation with its full message history."""
    try:
        conversation = Conversation.objects.get(id=conversation_id)
    except Conversation.DoesNotExist:
        return Response(
            {"error": "Conversation not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    return Response(ConversationSerializer(conversation).data)


@api_view(["POST"])
def conversation_ask(request, conversation_id):
    """Ask a question within a conversation (RAG + history)."""
    try:
        conversation = Conversation.objects.get(id=conversation_id)
    except Conversation.DoesNotExist:
        return Response(
            {"error": "Conversation not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = AskQuestionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    question = serializer.validated_data["question"]

    if not DocumentChunk.objects.exists():
        return Response({
            "answer": "No study materials have been uploaded yet. Please upload documents first.",
            "sources": [],
        })

    try:
        answer, source_chunks = ask_with_rag(question, conversation)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response({
        "answer": answer,
        "sources": [
            {
                "document": chunk["document_title"],
                "text_preview": chunk["chunk_text"][:200] + "..."
                    if len(chunk["chunk_text"]) > 200
                    else chunk["chunk_text"],
                "relevance_score": round(1 - chunk["distance"], 3),
            }
            for chunk in source_chunks
        ],
    })