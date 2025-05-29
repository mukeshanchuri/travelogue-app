from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv
import os
import json

# Load env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-pro",
    temperature=0.7,
    google_api_key=GOOGLE_API_KEY
)

# Prompt template
response_template = """
You are a smart and friendly travel assistant.

Your job is to create a short, engaging travel recommendation plan based on the user's goal and list of suggested places.

Tone: relaxed, casual, and inspiring — like a friendly local guide.

Instructions:
- Start with a short, 2-3 sentence intro based on the user's intent and context.
- Then list the recommended places using bullet points:
  - Each bullet should include: name, rating if available, and one unique detail.
  - Mention the general vibe or activity each place supports (e.g. "a peaceful garden for reflection").

Use markdown formatting for clarity.

---

Context:
{context}

Places:
{places}

Write the travel plan below:
"""

# Build prompt
response_prompt = PromptTemplate(
    input_variables=["context", "places"],
    template=response_template
)

# Chain: prompt -> llm
response_chain = response_prompt | llm

# Generator function
def generate_response(context: str, places: list) -> str:
    # Parse JSON if context looks like JSON
    if isinstance(context, str):
        try:
            if context.strip().startswith("{") and context.strip().endswith("}"):
                context = json.loads(context)
        except json.JSONDecodeError:
            pass

    # Format context
    context_str = (
        json.dumps(context, indent=2) if isinstance(context, dict) else str(context)
    )

    # Format places into markdown bullets
    place_lines = []
    for place in places:
        name = place.get("name", "Unknown Place")
        rating = place.get("rating", "N/A")
        address = place.get("address", "Unknown address")
        types = place.get("type", ["local attraction"])
        highlight = types[0].replace("_", " ").title() if types else "a local highlight"
        line = f"- **{name} ({rating}⭐)** – {highlight}, located at {address}"
        place_lines.append(line)

    # Prepare inputs
    inputs = {
        "context": context_str,
        "places": "\n".join(place_lines)
    }

    # Call Gemini LLM
    result = response_chain.invoke(inputs)

    # Handle response format
    if hasattr(result, "content"):
        return result.content
    elif isinstance(result, dict) and "content" in result:
        return result["content"]
    else:
        return str(result)

# End of file
# All rights reserved © 2025 by Mukesh Anchuri. Unauthorized use is prohibited. 