"""
Hybrid follow-up classifier.

1. Fast rule-based detection for obvious follow-up questions.
2. AI-based fallback using Phi-3 (Ollama).
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
    "before"
}

SYSTEM_PROMPT = """
You are a conversation classifier.

Determine whether the user's message depends on previous conversation.

Examples

User: What is Kafka?
Answer: NO

User: Explain Docker.
Answer: NO

User: Who developed it?
Answer: YES

User: Compare it with RabbitMQ.
Answer: YES

User: Explain that again.
Answer: YES

User: Continue.
Answer: YES

Rules:
- Reply ONLY YES or NO.
- No explanation.
"""


def is_follow_up(prompt: str) -> bool:
    """
    Returns True if the prompt appears to depend
    on previous conversation.
    """

    prompt = prompt.strip().lower()

    words = prompt.replace("?", "").replace(".", "").split()

    # ------------------------------------------------------
    # Fast rule-based detection
    # ------------------------------------------------------

    if any(word in FOLLOW_UP_KEYWORDS for word in words):
        return True

    # ------------------------------------------------------
    # AI-based fallback
    # ------------------------------------------------------

    try:

        response = chat(
            model="phi3:latest",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
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