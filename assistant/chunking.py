def chunk_text(text, max_chunk_size=800):
    """
    Split text into chunks using paragraph boundaries.

    Packs paragraphs together until a chunk reaches max_chunk_size,
    then starts a new chunk.
    """
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        # If adding this paragraph would exceed the limit, save current chunk
        if current_chunk and len(current_chunk) + len(paragraph) + 2 > max_chunk_size:
            chunks.append(current_chunk)
            current_chunk = paragraph
        else:
            if current_chunk:
                current_chunk += "\n\n" + paragraph
            else:
                current_chunk = paragraph

    # Don't forget the last chunk
    if current_chunk:
        chunks.append(current_chunk)

    return chunks