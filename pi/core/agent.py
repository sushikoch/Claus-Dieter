from anthropic import Anthropic
from pi.core.config import OPENROUTER_API_KEY, OPENROUTER_MODEL

client = Anthropic(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

def create_agent():
    system_prompt = """Du bist Pi, ein persönlicher Voice-Assistent für macOS.
Du hilfst mit Kalender, E-Mail, Apps und anderen Office-Tasks.
Beantworte Fragen präzise und nutze Tools wenn nötig."""

    return {"messages": [], "system": system_prompt}

def chat(agent, user_message):
    agent["messages"].append({"role": "user", "content": user_message})

    response = client.messages.create(
        model=OPENROUTER_MODEL,
        max_tokens=1024,
        system=agent["system"],
        messages=agent["messages"],
    )

    assistant_message = response.content[0].text
    agent["messages"].append({"role": "assistant", "content": assistant_message})

    return assistant_message

def main():
    agent = create_agent()

    print("Pi – Persönlicher Assistent (Text-Loop)")
    print("Tippe 'exit' zum Beenden\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            break

        if not user_input:
            continue

        response = chat(agent, user_input)
        print(f"Pi: {response}\n")

if __name__ == "__main__":
    main()
