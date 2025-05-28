from datetime import datetime
from utils.weather_api import get_weather_forecast
from utils.memory_store import get_user_preferences

def build_context(location: str, intent: str) -> str:
    """
    Builds a natural language context string including location, intent, time, weather, and user preferences.
    """
    current_time = datetime.now().strftime("%I:%M %p")
    weather = get_weather_forecast(location)
    memory = get_user_preferences()

    context = (
        f"The user is currently in {location} and wants to {intent}.\n"
        f"The current time is {current_time}.\n"
        f"The weather is {weather}.\n"
        f"Based on past preferences: {memory}."
    )

    return context
