# list_models.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load your .env variables
load_dotenv()

# Configure with your API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Fetch and print all available models
models = genai.list_models()
print("Available models:")
for m in models:
    print(f"  {m.name}  —  supported methods: {m.supported_generation_methods}")
