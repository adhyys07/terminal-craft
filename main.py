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
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        res_json = response.json()
        return res_json["choices"][0]["message"]["content"]
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
            new_model = choose_model(models)
            if new_model:
                model_id = new_model
                print(f"Switched to model: {model_id}\n")
            else:
                print("Model change cancelled.\n")
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
