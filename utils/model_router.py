# utils/model_router.py

def select_model(user_input: str) -> str:
    """
    Dynamically choose a model based on user intent or keywords.
    """
    user_input = user_input.lower()

    if "summarize" in user_input or "analyze" in user_input:
        return "claude"
    elif "weather" in user_input or "map" in user_input or "live" in user_input:
        return "gemini"
    elif "travel" in user_input or "recommend" in user_input:
        return "gemini"
    else:
        return "gemini"  # fallback
