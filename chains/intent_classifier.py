from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv
import os

# Debug marker to ensure correct file is loaded
print(">>> Running UPDATED intent_classifier.py <<<")

# Load environment variables from .env
load_dotenv()

# Initialize Gemini model from Google
llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-pro",
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Load prompt template text from file
with open("prompts/intent_prompt.txt", "r", encoding="utf-8") as f:
    template = f.read()

# Build a prompt template that expects an 'input' variable
intent_prompt = PromptTemplate(
    input_variables=["input"],
    template=template
)

# Build chain using the modern LangChain pipe syntax
intent_chain = intent_prompt | llm

def classify_intent(user_input: str) -> str:
    """
    Classifies the user's travel intent and strips any 'intent:' label.
    """
    # Invoke the prompt-chain with the user's input
    result = intent_chain.invoke({"input": user_input})

    # Handle different response formats from the LLM
    if isinstance(result, dict) and "content" in result:
        raw = result["content"]
    elif hasattr(result, "content"):
        raw = result.content
    else:
        raw = str(result)

    # Clean the output by removing the label and trimming whitespace
    cleaned = raw.lower().replace("intent:", "").strip()
    return cleaned
