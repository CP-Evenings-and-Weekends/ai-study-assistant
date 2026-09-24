from django.db import models
from pgvector.django import VectorField


class Document(models.Model):
    """A study document uploaded by the user."""
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class DocumentChunk(models.Model):
    """A chunk of a document with its embedding for vector search."""
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="chunks"
    )
    chunk_text = models.TextField()
    chunk_index = models.IntegerField()
    embedding = VectorField(dimensions=768)

    class Meta:
        ordering = ["document", "chunk_index"]

    def __str__(self):
        return f"{self.document.title} - Chunk {self.chunk_index}"