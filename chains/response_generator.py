from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv
import os

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

Given the context of the user's intent and a list of relevant places, generate a short, engaging travel narrative.

Use a relaxed and casual tone. Highlight each place with bullet points, including name, rating if available, and one unique highlight.

Context:
{context}

Places:
{places}

Respond with a travel recommendation plan.
"""

# Build prompt
response_prompt = PromptTemplate(
    input_variables=["context", "places"],
    template=response_template
)

# Chain: prompt -> llm
response_chain = response_prompt | llm

# Generator function
# Generator function
def generate_response(context: str, places: list) -> str:
    import json

    # Try to parse JSON only if it looks like a JSON object
    if isinstance(context, str):
        try:
            if context.strip().startswith("{") and context.strip().endswith("}"):
                context = json.loads(context)
        except json.JSONDecodeError:
            pass  # Keep context as raw string if not valid JSON

    # Format context for the prompt
    context_str = (
        json.dumps(context, indent=2) if isinstance(context, dict) else str(context)
    )

    # Format places list
    place_lines = []
    for place in places:
        name = place.get("name", "Unknown Place")
        rating = place.get("rating", "N/A")
        address = place.get("address", "Unknown address")
        highlight = place.get("type", ["local attraction"])[0].replace("_", " ").title()
        line = f"- **{name} ({rating}⭐)** – {highlight}, located at {address}"
        place_lines.append(line)

    # Compose input for LLM
    inputs = {
        "context": context_str,
        "places": "\n".join(place_lines)
    }

    # Run through LangChain chain
    result = response_chain.invoke(inputs)

    # Handle response format
    if hasattr(result, "content"):
        return result.content
    elif isinstance(result, dict) and "content" in result:
        return result["content"]
    else:
        return str(result)


# End of file
# All rights reserved © 2025 by Mukesh. Unauthorized use is prohibited.
