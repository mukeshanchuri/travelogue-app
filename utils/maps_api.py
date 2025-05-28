from chains.place_fetcher import fetch_places

location = "Jaipur"
intent = "explore"

places = fetch_places(location, intent)

for p in places:
    print(f"{p['name']} ({p['rating']}⭐)\n{p['address']}\n")

