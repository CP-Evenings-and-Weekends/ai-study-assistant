from django.db import migrations
from pgvector.django import VectorExtension


class Migration(migrations.Migration):
    """Enable the pgvector extension before any vector columns are created.

    When you run `makemigrations` after writing your models, Django will
    create a 0002 migration that depends on this one, so the extension is
    always in place before your VectorField columns exist.
    """

    initial = True

    dependencies = []

    operations = [
        VectorExtension(),
    ]
