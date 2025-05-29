from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

from utils.weather_api import get_weather_forecast
from utils.memory_store import get_user_preferences


def get_local_time(location_name: str) -> str:
    """
    Converts location name into local time using geolocation and timezone APIs.
    """
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


def build_context(location: str, intent: str) -> dict:
    """
    Gathers time, weather, and user preferences into a structured context dictionary.
    """
    local_time  = get_local_time(location)
    weather     = get_weather_forecast(location)
    memory      = get_user_preferences()

    return {
        "location": location,
        "intent":   intent,
        "time":     local_time,
        "weather":  weather,
        "memory":   memory
    }
