from groq import Groq
from core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

SYSTEM_PROMPT = """
You rewrite follow-up questions into complete standalone questions.

Use the previous conversation.

Do NOT answer the question.

Only rewrite it.

Example

Conversation:
User: Top universities for finance in Germany

Current:
and UK

Output:
Top universities for finance in the UK.

------------------

Conversation:
User: Explain Python

Current:
its advantages

Output:
What are the advantages of Python?

------------------

Conversation:
User: Compare Kafka and RabbitMQ

Current:
pricing

Output:
Compare the pricing of Kafka and RabbitMQ.
"""

def rewrite_query(
    conversation: list,
    prompt: str,
) -> str:

    history = ""

    for m in conversation[-6:]:
        history += f'{m["role"]}: {m["content"]}\n'

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": f"""
Conversation

{history}

Current

{prompt}
""",
            },
        ],
    )

    return response.choices[0].message.content.strip()