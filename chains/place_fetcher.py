import requests
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def get_coordinates(location: str):
    geo_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": location, "key": API_KEY}

    # DEBUGGING
    print(f"🌐 Geocoding location: {location}")
    print(f"🔑 Using API Key: {API_KEY[:6]}******")  # Masked for safety

    resp = requests.get(geo_url, params=params)
    data = resp.json()

    # DEBUGGING
    print("📦 Geocode API full response:", data)

    results = data.get("results", [])
    if not results:
        print(f"❌ Could not geocode location: {location}")
        return None, None
    loc = results[0]["geometry"]["location"]
    return loc["lat"], loc["lng"]



def fetch_places(location: str, intent: str, max_results: int = 5) -> list:
    """
    Uses Google Places Text Search API to find top places for a given intent near a location.
    """
    query_map = {
        "explore":  "tourist attractions",
        "eat":      "best restaurants",
        "chill":    "quiet places to relax",
        "cultural": "museums or art galleries",
        "avoid":    "overrated places"
    }

    search_term = query_map.get(intent, "things to do")

    # Get coordinates for more accurate search
    lat, lng = get_coordinates(location)
    if not lat or not lng:
        return []

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": search_term,
        "location": f"{lat},{lng}",
        "radius": 5000,
        "key": API_KEY
    }

    resp = requests.get(url, params=params)
    data = resp.json().get("results", [])

    results = []
    for place in data[:max_results]:
        results.append({
            "name":    place.get("name"),
            "rating":  place.get("rating", "N/A"),
            "address": place.get("formatted_address"),
            "type":    place.get("types", [])
        })

    return results
