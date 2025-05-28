# cli.py

import warnings
from chains.intent_classifier import classify_intent
from chains.context_builder import build_context
from chains.place_fetcher import fetch_places
from chains.response_generator import generate_response

# ── suppress deprecation and user warnings ──
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

def main():
    print("\n👋 Welcome to Travel’logue – Your Smart Travel Companion!\n")
    user_location = input("📍 Where are you right now? ")
    user_goal = input(
        "✨ How do you want me to plan your day?\n"
        "(e.g., 'I want to eat good street food' or 'find calm places')\n> "
    )

    # 1) Classify Intent
    intent = classify_intent(user_goal)
    print(f"🧠 Detected intent: {intent}")

    # 2) Build Context
    context = build_context(user_location, intent)

    # 3) Fetch Places
    places = fetch_places(user_location, intent)
    print(f"📌 Found {len(places)} interesting places for you!")

    # 4) Generate Travel Narrative
    response = generate_response(context, places)

    # Final Output
    print("\n🗺️ Here's your travel plan:\n")
    print(response)
    print("\n✅ Done. Need another plan? Rerun me!\n")

if __name__ == "__main__":
    main()
