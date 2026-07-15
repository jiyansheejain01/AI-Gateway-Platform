"""
Hybrid follow-up classifier.

1. Fast rule-based detection for obvious follow-up questions.
2. AI-based fallback using Phi-3 (Ollama) with conversation context.
"""

from ollama import chat


# ----------------------------------------------------------
# Rule-based follow-up keywords
# ----------------------------------------------------------

FOLLOW_UP_KEYWORDS = {
    "it",
    "its",
    "they",
    "them",
    "their",
    "this",
    "that",
    "these",
    "those",
    "he",
    "she",
    "him",
    "her",
    "again",
    "continue",
    "more",
    "also",
    "another",
    "previous",
    "above",
    "earlier",
    "before",

    # Common conversational follow-ups
    "and",
    "what",
    "why",
    "how",
    "which",
    "where",
    "when",
    "compare",
    "versus",
    "vs",
    "fees",
    "cost",
    "ranking",
}


SYSTEM_PROMPT = """
You are a conversation classifier.

You will receive:

1. Previous conversation.
2. Current user message.

Determine whether the current message depends on the previous conversation.

Examples

Conversation

User: Top universities in Germany

Current:
and UK

Answer:
YES


Conversation

User: Explain Kafka

Current:
What is Docker?

Answer:
NO


Conversation

User: Explain CNN

Current:
Advantages?

Answer:
YES


Conversation

User: Weather in Delhi

Current:
Bangalore?

Answer:
YES


Rules

- Reply ONLY YES or NO.
- No explanation.
"""


def is_follow_up(
    prompt: str,
    conversation: list,
) -> bool:

    prompt = prompt.strip()

    words = (
        prompt.lower()
        .replace("?", "")
        .replace(".", "")
        .split()
    )

    # ------------------------------------------------------
    # Rule 1: Very short prompts are almost always follow-ups
    # ------------------------------------------------------

    if len(words) <= 3:
        return True

    # ------------------------------------------------------
    # Rule 2: Keyword detection
    # ------------------------------------------------------

    if any(word in FOLLOW_UP_KEYWORDS for word in words):
        return True

    # ------------------------------------------------------
    # Rule 3: AI Classification
    # ------------------------------------------------------

    try:

        history = ""

        for message in conversation[-6:]:

            history += (
                f'{message["role"]}: '
                f'{message["content"]}\n'
            )

        response = chat(
            model="phi3:latest",
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

        answer = (
            response["message"]["content"]
            .strip()
            .upper()
        )

        return answer.startswith("YES")

    except Exception as e:

        print("Follow-up classifier error:", e)

        return False