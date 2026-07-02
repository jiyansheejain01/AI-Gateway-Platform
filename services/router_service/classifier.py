"""
Advanced rule-based prompt complexity classifier.
Returns a complexity score and category.
"""


def classify_prompt(prompt: str) -> dict:

    prompt_lower = prompt.lower()

    score = 0

    words = prompt.split()
    word_count = len(words)

    # -----------------------------
    # 1. Prompt Length (20)
    # -----------------------------
    if word_count > 150:
        score += 20
    elif word_count > 80:
        score += 15
    elif word_count > 40:
        score += 10
    elif word_count > 20:
        score += 5

    # -----------------------------
    # 2. Number of Sentences (15)
    # -----------------------------
    sentence_count = (
        prompt.count(".")
        + prompt.count("?")
        + prompt.count("!")
    )

    if sentence_count >= 8:
        score += 15
    elif sentence_count >= 5:
        score += 10
    elif sentence_count >= 3:
        score += 5

    # -----------------------------
    # 3. Reasoning Keywords (35)
    # -----------------------------
    reasoning_keywords = [
        "design",
        "architect",
        "compare",
        "evaluate",
        "justify",
        "optimize",
        "implement",
        "analyze",
        "analyse",
        "discuss",
        "recommend",
        "strategy",
        "approach",
        "build",
        "develop",
        "step by step",
        "system design",
        "trade-off",
        "tradeoff"
    ]

    score += min(
        35,
        sum(
            5
            for keyword in reasoning_keywords
            if keyword in prompt_lower
        )
    )

    # -----------------------------
    # 4. Technical Concepts (30)
    # -----------------------------
    technical_keywords = [
        "distributed",
        "microservices",
        "kubernetes",
        "docker",
        "kafka",
        "redis",
        "qdrant",
        "vector database",
        "embedding",
        "rag",
        "transformer",
        "llm",
        "machine learning",
        "deep learning",
        "database",
        "fault tolerance",
        "high availability",
        "replication",
        "sharding",
        "load balancing",
        "consensus",
        "raft",
        "paxos",
        "api gateway"
    ]

    score += min(
        30,
        sum(
            5
            for keyword in technical_keywords
            if keyword in prompt_lower
        )
    )

    # -----------------------------
    # Final Score
    # -----------------------------
    score = min(score, 100)

    if score >= 40:
        category = "complex"
    else:
        category = "simple"

    return {
        "score": score,
        "category": category
    }