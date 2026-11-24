
import os
import psycopg
from psycopg.rows import dict_row


def get_documents():
    connection_string = os.getenv(
        "DATABASE_URL",
        "dbname=hospital_ai"
    )

    with psycopg.connect(
        connection_string,
        row_factory=dict_row
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, title, filename FROM documents"
            )

            return cursor.fetchall()



def save_document(filename: str, pages: list):
    from document_service import split_text

    connection_string = os.getenv(
        "DATABASE_URL",
        "dbname=hospital_ai"
    )

    full_text = "\n".join(
        page["content"] for page in pages
    )

    with psycopg.connect(connection_string) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO documents
                    (filename, title, content)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (filename, filename, full_text)
            )

            document_id = cursor.fetchone()[0]
            total_chunks = 0

            for page in pages:
                chunks = split_text(page["content"])

                for index, chunk in enumerate(chunks):
                    cursor.execute(
                        """
                        INSERT INTO document_chunks
                            (document_id, page_number,
                             chunk_index, content)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (
                            document_id,
                            page["page_number"],
                            index,
                            chunk
                        )
                    )
                    total_chunks += 1

    return {
        "document_id": document_id,
        "chunks_created": total_chunks
    }
