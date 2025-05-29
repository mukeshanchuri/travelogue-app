import streamlit as st
from chains.intent_classifier import classify_intent
from chains.context_builder import build_context
from chains.place_fetcher import fetch_places
from chains.response_generator import generate_response

st.set_page_config(page_title="Travel’logue", page_icon="🌍", layout="centered")
st.title("🌍 Travel’logue – Your Smart Travel Companion")

# Initialize session history
if "history" not in st.session_state:
    st.session_state.history = []

# Cached versions of key functions
@st.cache_data(show_spinner=False)
def cached_classify_intent(goal):
    return classify_intent(goal)

@st.cache_data(show_spinner=False)
def cached_build_context(location, intent, preferences):
    context = build_context(location, intent)
    if preferences:
        joined = ", ".join([p.lower() for p in preferences])
        context += f"\nThe user also prefers: {joined}."
    return context

@st.cache_data(show_spinner=False)
def cached_fetch_places(location, intent):
    return fetch_places(location, intent)

# Step 1: User inputs
location = st.text_input("📍 Where are you right now?")
goal = st.text_input(
    "✨ How would you like to spend your day?",
    help="E.g., 'I want to explore historical places' or 'find quiet cafés'"
)

# Step 2: Multiple travel preferences
preferences = st.multiselect(
    "🎯 Any travel preferences?",
    [
        "🌞 Best time to visit",
        "🚫 Avoid crowded places",
        "🧒 Kid-friendly options",
        "💰 Budget-friendly",
        "🧘 Peaceful spots"
    ],
    help="Choose one or more filters to tailor your trip"
)

# Step 3: Action trigger
if st.button("🧭 Plan My Day"):
    if not location or not goal:
        st.warning("Please enter both your location and travel goal.")
    else:
        st.subheader("🧠 Detecting Your Intent...")
        intent = cached_classify_intent(goal)
        st.success(f"Intent Detected: **{intent}**")

        # Build context (string)
        context = cached_build_context(location, intent, preferences)

        # Fetch relevant places
        places = cached_fetch_places(location, intent)

        if not places:
            st.error("❌ No places found. Try adjusting your input.")
        else:
            st.success(f"📍 Found {len(places)} places for you!")

            try:
                response = generate_response(context, places, location, goal, intent, preferences)
                st.markdown("### 🗺️ Your Travel Plan:")
                st.markdown(response)
                except Exception as e:
                    st.error("⚠️ Oops! Something went wrong while generating your travel plan.")
                    st.code(str(e))
            # Save to history
            st.session_state.history.append({
                "location": location,
                "goal": goal,
                "intent": intent,
                "preferences": preferences,
                "response": response
            })

# Step 4: Show session history
if st.session_state.history:
    st.markdown("## 🕘 Your Previous Plans")
    for i, entry in enumerate(reversed(st.session_state.history), 1):
        with st.expander(f"Plan #{i}: {entry['goal']} in {entry['location']}"):
            st.markdown(f"**Intent:** {entry['intent']}")
            if entry.get("preferences"):
                prefs = ", ".join(entry["preferences"])
                st.markdown(f"**Preferences:** {prefs}")
            st.markdown(entry['response'])

st.markdown("---")
st.markdown("© 2025 Mukesh Anchuri. All rights reserved.", unsafe_allow_html=True)
