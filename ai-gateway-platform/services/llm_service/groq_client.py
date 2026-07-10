from groq import Groq

from core.config import settings

client = Groq(
    api_key=settings.GROQ_API_KEY
)


def generate(messages):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.3,
    )

    return {
        "response": response.choices[0].message.content,
        "model": "llama-3.1-8b-instant",
    }