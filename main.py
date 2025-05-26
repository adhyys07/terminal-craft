import requests

def get_api_key():
    return input("Enter your Groq API key: ").strip()

def list_models(api_key):
    url = "https://api.groq.com/openai/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        models = data.get("data", [])

        # Remove models at positions: 3,5,6,10,15,17,18,19,20 (0-based: 2,4,5,9,14,16,17,18,19)
        exclude_indices = {2, 4, 5, 9, 14, 16, 17, 18, 19}
        models = [m for i, m in enumerate(models) if i not in exclude_indices]

        return models
    except Exception as e:
        print(f"Error fetching models: {e}")
        return []

def choose_model(models):
    print("\nAvailable Groq Models:\n")
    for i, model in enumerate(models, 1):
        print(f"{i}. {model['id']}")
    choice = input("\nChoose a model by number: ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(models):
        print("Invalid choice.")
        return None
    return models[int(choice) - 1]["id"]

def call_groq(api_key, model_id, prompt):
    # Determine correct endpoint
    if "llama" in model_id or "chat" in model_id:
        url = "https://api.groq.com/openai/v1/chat/completions"
        data = {
            "model": model_id,
            "messages": [{"role": "user", "content": prompt}]
        }
    else:
        url = "https://api.groq.com/openai/v1/completions"
        data = {
            "model": model_id,
            "prompt": prompt,
            "max_tokens": 100,
            "temperature": 0.7
        }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        res_json = response.json()

        if "choices" in res_json:
            if "chat" in url:
                return res_json["choices"][0]["message"]["content"]
            else:
                return res_json["choices"][0]["text"]
        return "Unexpected response format."

    except Exception as e:
        return f"API error: {e}"

def main():
    print("Groq AI CLI\n")
    api_key = get_api_key()

    models = list_models(api_key)
    if not models:
        print("No models found or failed to fetch models.")
        return

    model_id = choose_model(models)
    if not model_id:
        return

    print("\nType your prompt and press Enter to get a response.")
    print("Type '/change' to change AI model, or '/exit' to quit.\n")

    while True:
        prompt = input("> ").strip()
        if prompt.lower() == "/exit":
            print("Exiting... Goodbye!")
            break
        elif prompt.lower() == "/change":
            model_id = choose_model(models)
            if not model_id:
                print("Model change cancelled.")
                continue
            print(f"Switched to model: {model_id}\n")
            continue
        elif prompt == "":
            continue

        print("\n⏳ Generating response...\n")
        response = call_groq(api_key, model_id, prompt)
        print("✅ Response:\n")
        print(response)
        print("\n---\n")

if __name__ == "__main__":
    main()
