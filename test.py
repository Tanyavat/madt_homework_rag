import google.generativeai as genai

# Your MakerSuite API Key (not a JSON, just a string like "AIza...")
genai.configure(api_key="AIza...")

print("✅ Checking available models with your API key...\n")

try:
    models = genai.list_models()
    for model in models:
        print(f"Model: {model.name}")
        print(f"  Supported methods: {model.supported_generation_methods}")
        print()
except Exception as e:
    print("❌ Failed to list models.")
    print(e)
