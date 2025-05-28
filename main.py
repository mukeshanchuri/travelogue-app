import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

from chains.intent_classifier import classify_intent
from chains.context_builder import build_context
from chains.place_fetcher import fetch_places
from chains.response_generator import generate_response

def main():
    print("\n👋 Welcome to Travel’logue – Your Smart Travel Companion!\n")
    
    # Step 1: Get and clean user inputs
    user_location = input("📍 Where are you right now? ").strip()
    user_goal = input(
        "✨ How do you want me to plan your day? "
        "(e.g., 'I want to eat good street food' or 'find calm places')\n> "
    ).strip()

    # Debug: Confirm user inputs
    print(f"🔍 Location received: '{user_location}'")
    print(f"🔍 Goal received: '{user_goal}'")

    # Step 2: Classify the intent
    intent = classify_intent(user_goal)
    print(f"🧠 Detected intent: {intent}")

    # Step 3: Build context using location + intent
    context = build_context(user_location, intent)

    # Step 4: Fetch relevant places using Google Maps API
    places = fetch_places(user_location, intent)
    if not places:
        print("⚠️ Sorry, no places were found. Please try a different request or check your API.")
        return
    print(f"📌 Found {len(places)} interesting places for you!")

    # Step 5: Generate a custom travel plan or response
    response = generate_response(context, places)

    # Step 6: Output the final travel plan
    print("\n🗺️ Here's your travel plan:\n")
    print(response)
    print("\n✅ Done. Need another plan? Rerun me!\n")

if __name__ == "__main__":
    main()
