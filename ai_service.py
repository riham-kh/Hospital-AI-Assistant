
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
You are a helpful hospital administrative assistant.

Rules:
- Answer clearly and concisely.
- Do not invent hospital policies.
- If you are unsure, say so.
- Do not provide patient-specific medical advice.
- Encourage users to verify official procedures.
"""


def generate_answer(question: str) -> str:
    response = client.responses.create(
        model="gpt-6-luna",
        instructions=SYSTEM_PROMPT,
        input=question
    )

    return response.output_text
