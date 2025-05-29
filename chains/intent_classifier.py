from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv
import os

# Debug marker
print(">>> Running UPDATED intent_classifier.py <<<")

# Load environment variables
load_dotenv()

# Check for missing API key early
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY is missing in your .env file!")

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-pro",
    temperature=0.5,
    google_api_key=GOOGLE_API_KEY
)

# Load prompt template
with open("prompts/intent_prompt.txt", "r", encoding="utf-8") as f:
    template = f.read()

# Prompt template expects one input variable: `input`
intent_prompt = PromptTemplate(
    input_variables=["input"],
    template=template
)

# Create runnable chain
intent_chain = intent_prompt | llm

def classify_intent(user_input: str) -> str:
    """
    Classifies the user's travel intent and strips any prefix like 'intent:'.
    """
    try:
        result = intent_chain.invoke({"input": user_input})
    except Exception as e:
        print("❌ Error invoking LLM:", e)
        return "unknown"

    # Handle different LLM output structures
    if isinstance(result, dict) and "content" in result:
        raw = result["content"]
    elif hasattr(result, "content"):
        raw = result.content
    else:
        raw = str(result)

    # Clean and standardize output
    cleaned = raw.lower().replace("intent:", "").strip()
    return cleaned
