import os
from langsmith import traceable
from langsmith.wrappers import wrap_openai
from openai import OpenAI
from dotenv import load_dotenv

# Configuration: Load environment variables from .env
# Required: LANGSMITH_TRACING="true", LANGSMITH_API_KEY, OPENAI_API_KEY
load_dotenv()

# OpenAI Wrapper: Automatically captures token usage, model names, and costs.
client = wrap_openai(OpenAI(api_key=os.getenv("OPENAI_API_KEY")))


# =============================================================================
# EXAMPLE 1: Simple Trace - Single LLM Call
# =============================================================================
# This is the simplest case: one function, one LLM call.
# The trace will have a single generation inside it.


@traceable(name="Simple Question")
def ask_simple_question(question: str) -> str:
    """A simple trace with just one LLM call."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": question}],
    )
    return response.choices[0].message.content


# =============================================================================
# EXAMPLE 2: LLM Call + Custom Python Logic
# =============================================================================
# This shows how to trace a workflow that combines an LLM call
# with post-processing logic (e.g., parsing, validation, transformation).


@traceable(name="Extract Keywords")
def extract_keywords(text: str) -> list[str]:
    """LLM extracts keywords, then Python processes the result."""

    # Step 1: LLM call to extract keywords
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Extract 5 keywords from the text. Return only the keywords, comma-separated.",
            },
            {"role": "user", "content": text},
        ],
    )
    raw_keywords = response.choices[0].message.content

    # Step 2: Custom Python logic to clean and format
    keywords = [kw.strip().lower() for kw in raw_keywords.split(",")]
    keywords = [kw for kw in keywords if len(kw) > 2]  # Filter short words

    return keywords


# =============================================================================
# EXAMPLE 3: Multi-Step Pipeline - Multiple LLM Calls
# =============================================================================
# This demonstrates a complex trace with nested spans and multiple generations.
# Common pattern: Generate → Critique → Refine


@traceable(name="Step 1: Generate Draft")
def generate_draft(topic: str) -> str:
    """First LLM call: Generate initial content."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful writing assistant."},
            {"role": "user", "content": f"Write a short paragraph about: {topic}"},
        ],
    )
    return response.choices[0].message.content


@traceable(name="Step 2: Critique Draft")
def critique_draft(draft: str) -> str:
    """Second LLM call: Analyze the draft for improvements."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a writing critic. Provide 2-3 brief suggestions to improve this text.",
            },
            {"role": "user", "content": draft},
        ],
    )
    return response.choices[0].message.content


@traceable(name="Step 3: Refine Draft")
def refine_draft(draft: str, critique: str) -> str:
    """Third LLM call: Apply the critique to improve the draft."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Rewrite the text based on the feedback provided.",
            },
            {
                "role": "user",
                "content": f"Original:\n{draft}\n\nFeedback:\n{critique}\n\nRewrite:",
            },
        ],
    )
    return response.choices[0].message.content


@traceable(name="Content Refinement Pipeline")
def content_pipeline(topic: str) -> dict:
    """Parent trace that orchestrates the multi-step workflow."""
    draft = generate_draft(topic)
    critique = critique_draft(draft)
    final = refine_draft(draft, critique)

    return {
        "draft": draft,
        "critique": critique,
        "final": final,
    }


# =============================================================================
# MAIN: Run all three examples
# =============================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("EXAMPLE 1: Simple Question (Single LLM Call)")
    print("=" * 60)
    answer = ask_simple_question("What is the capital of France?")
    print(f"Answer: {answer}\n")

    print("=" * 60)
    print("EXAMPLE 2: Extract Keywords (LLM + Python Logic)")
    print("=" * 60)
    text = "Machine learning is a subset of artificial intelligence that enables computers to learn from data without being explicitly programmed."
    keywords = extract_keywords(text)
    print(f"Keywords: {keywords}\n")

    print("=" * 60)
    print("EXAMPLE 3: Content Pipeline (Multiple LLM Calls)")
    print("=" * 60)
    result = content_pipeline("the importance of sleep for productivity")
    print(f"Draft: {result['draft'][:100]}...")
    print(f"Critique: {result['critique'][:100]}...")
    print(f"Final: {result['final'][:100]}...")

    print("\nAll traces sent to LangSmith. Check your dashboard!")
