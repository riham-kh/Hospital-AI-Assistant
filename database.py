
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
