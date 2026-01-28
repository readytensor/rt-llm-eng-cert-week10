"""
Simple chat client for LiteLLM proxy with custom chat template.

Usage:
    python client.py "Summarize this text: Machine learning is amazing."
    python client.py  # Interactive mode
"""

import sys
from openai import OpenAI
from transformers import AutoTokenizer

# Configuration
LITELLM_URL = "http://localhost:4000"
# LITELLM_KEY = "sk-litellm-master-key"
LITELLM_KEY = "sk-OiSJqUdCXvSfUuj6aIfoGw"
MODEL_NAME = "lora-summarizer"
TOKENIZER_ID = "moo3030/Llama-3.2-1B-Summarizer-merged"

# Initialize clients
client = OpenAI(base_url=LITELLM_URL, api_key=LITELLM_KEY)
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_ID)


def apply_chat_template(user_message: str) -> str:
    """Apply the model's chat template to format the prompt."""
    messages = [{"role": "user", "content": user_message}]

    # Apply chat template (returns formatted string)
    formatted = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    return formatted


def send_request(prompt: str, max_tokens: int = 256) -> str:
    """Send request to LiteLLM proxy."""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.7,
    )
    return response.choices[0].message.content


def main():
    print(f"Connected to: {LITELLM_URL}")
    print(f"Model: {MODEL_NAME}")
    print(f"Tokenizer: {TOKENIZER_ID}")
    print("-" * 50)

    # Check if input provided as argument
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        formatted_prompt = apply_chat_template(user_input)
        print(f"\nInput: {user_input[:100]}...")
        print(f"\nFormatted prompt:\n{formatted_prompt[:200]}...")
        print("\nSending request...")

        response = send_request(user_input)
        print(f"\nResponse:\n{response}")
    else:
        # Interactive mode
        print("Interactive mode. Type 'quit' to exit.\n")

        while True:
            try:
                user_input = input("You: ").strip()

                if user_input.lower() in ["quit", "exit", "q"]:
                    print("Goodbye!")
                    break

                if not user_input:
                    continue

                formatted_prompt = apply_chat_template(user_input)
                print(f"\n[Formatted: {formatted_prompt[:100]}...]\n")

                response = send_request(user_input)
                print(f"Bot: {response}\n")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break


if __name__ == "__main__":
    main()
