from datetime import datetime
from utils.weather_api import get_weather_forecast
from utils.memory_store import get_user_preferences

def build_context(location: str, intent: str) -> dict:
    """
    Gathers time, weather, and user preferences into a context dict.
    """
    current_time = datetime.now().strftime("%I:%M %p")
    weather      = get_weather_forecast(location)
    memory       = get_user_preferences()

    return {
        "location": location,
        "intent":   intent,
        "time":     current_time,
        "weather":  weather,
        "memory":   memory
    }


from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz

def get_local_time(location_name: str) -> str:
    geolocator = Nominatim(user_agent="travelogue-app")
    location = geolocator.geocode(location_name)

    if not location:
        return "local time unavailable"

    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lat=location.latitude, lng=location.longitude)

    if timezone_str:
        timezone = pytz.timezone(timezone_str)
        local_time = datetime.now(timezone)
        return local_time.strftime("%A, %d %B %Y at %I:%M %p %Z")
    
    return "local time unavailable"

def build_context(location: str, intent: str) -> str:
    time_info = get_local_time(location)

    context = (
        f"The user is in {location}, and their intent is: {intent.lower()}.\n"
        f"The current local time in {location} is {time_info}."
    )
    
    return context
