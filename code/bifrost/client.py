"""
Bifrost Client - Interactive LLM Chat

This client connects to a Bifrost gateway, lists available models,
and allows the user to select a model and send prompts.

Commands:
  /model or /switch  - Switch to a different model
  /models or /list   - List all available models
  /current           - Show current model
  /help              - Show available commands
  quit, exit, q      - Exit the chat
"""

import requests

BIFROST_URL = "http://localhost:8080"


def list_models() -> list[str]:
    """Fetch available models from Bifrost."""
    try:
        response = requests.get(f"{BIFROST_URL}/v1/models")
        response.raise_for_status()
        data = response.json()
        models = [model["id"] for model in data.get("data", [])]
        return models
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to Bifrost. Is it running on port 8080?")
        return []
    except Exception as e:
        print(f"Error fetching models: {e}")
        return []


def send_message(model: str, message: str) -> str:
    """Send a message to the specified model via Bifrost."""
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": message}],
    }

    try:
        response = requests.post(
            f"{BIFROST_URL}/v1/chat/completions",
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.ConnectionError:
        return "Error: Cannot connect to Bifrost. Is it running?"
    except Exception as e:
        return f"Error: {e}"


def display_models(models: list[str]) -> None:
    """Display the list of available models."""
    print(f"\nAvailable models ({len(models)}):")
    print("-" * 40)
    for i, model in enumerate(models, 1):
        print(f"  {i}. {model}")
    print("-" * 40)


def select_model(
    models: list[str], prompt: str = "Select a model (enter number or full name): "
) -> str | None:
    """Let user select a model from the list."""
    while True:
        try:
            choice = input(prompt).strip()

            if not choice:
                return None

            # Check if user entered a number
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(models):
                    return models[idx]
                else:
                    print(f"Please enter a number between 1 and {len(models)}")
            else:
                # User entered a model name directly
                if choice in models or "/" in choice:
                    return choice
                else:
                    print(
                        f"Model '{choice}' not found. Try again or press Enter to cancel."
                    )
        except KeyboardInterrupt:
            return None


def show_help() -> None:
    """Display available commands."""
    print("\nAvailable commands:")
    print("  /model, /switch  - Switch to a different model")
    print("  /models, /list   - List all available models")
    print("  /current         - Show current model")
    print("  /help            - Show this help message")
    print("  quit, exit, q    - Exit the chat")
    print()


def main():
    print("=" * 50)
    print("Bifrost Client - Interactive LLM Chat")
    print("=" * 50)

    # Fetch available models
    print("\nFetching available models from Bifrost...")
    models = list_models()

    if not models:
        print("No models available. Please check your Bifrost configuration.")
        return

    display_models(models)

    # Let user select initial model
    selected_model = select_model(models, "\nSelect a model to start: ")
    if not selected_model:
        print("No model selected. Exiting.")
        return

    print(f"\nUsing model: {selected_model}")
    print("Type /help to see available commands.\n")

    # Chat loop
    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            if user_input.lower() in ["/help", "/h"]:
                show_help()
                continue

            if user_input.lower() in ["/models", "/list"]:
                models = list_models()  # Refresh the list
                display_models(models)
                continue

            if user_input.lower() in ["/current", "/c"]:
                print(f"Current model: {selected_model}\n")
                continue

            if user_input.lower() in ["/model", "/switch", "/m", "/s"]:
                models = list_models()  # Refresh the list
                display_models(models)
                new_model = select_model(models, "Switch to model: ")
                if new_model:
                    selected_model = new_model
                    print(f"Switched to: {selected_model}\n")
                else:
                    print("Model switch cancelled.\n")
                continue

            # Regular message - send to model
            print("Assistant: ", end="", flush=True)
            response = send_message(selected_model, user_input)
            print(response)
            print()

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
