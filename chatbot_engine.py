import json
import difflib

# Load the JSON data
with open("states_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Keyword variations for better matching
keyword_map = {
    "food": ["food", "eat", "cuisine", "dishes"],
    "weather": ["weather", "climate", "temperature"],
    "season": ["season", "best time", "visit"],
    "tourist_spots": ["tourist", "places", "spots", "visit", "attractions"],
    "culture": ["culture", "cultural", "tradition"],
    "history": ["history", "historical", "past"],
    "capital": ["capital", "main city"],
    "cities": ["cities", "major cities", "urban"],
    "languages": ["language", "languages", "speak"],
    "festivals": ["festival", "festivals", "celebration"],
    "transport": ["transport", "airport", "road", "reach"],
    "flora_fauna": ["flora", "fauna", "animals", "plants", "wildlife"],
    "traditional_dress": ["dress", "attire", "clothing", "wear"],
    "handicrafts": ["handicraft", "crafts", "artworks"],
    "unesco_or_fame": ["unesco", "famous", "popular", "well known"],
    "did_you_know": ["fact", "interesting", "did you know", "surprising"]
}

# Reverse keyword lookup
keyword_to_topic = {kw: topic for topic, kws in keyword_map.items() for kw in kws}

def extract_topics(message):
    message = message.lower()
    topics_found = set()
    for word in message.split():
        match = keyword_to_topic.get(word)
        if match:
            topics_found.add(match)
    return topics_found

def find_state_in_message(message):
    message = message.lower()
    states = list(data.keys())

    # First: try exact substring match
    for state in states:
        if state.lower() in message:
            return state

    # Second: try close match against whole message
    close_matches = difflib.get_close_matches(message, states, n=1, cutoff=0.5)
    if close_matches:
        return close_matches[0]

    # Third: check word-by-word fuzzy matching
    for word in message.split():
        close = difflib.get_close_matches(word.capitalize(), states, n=1, cutoff=0.6)
        if close:
            return close[0]
    return None

def format_topic_data(info, topic):
    if topic in ["tourist_spots", "cities", "languages", "festivals", "handicrafts", "did_you_know"]:
        return f"📌 {topic.replace('_', ' ').title()}: {', '.join(info.get(topic, []))}"
    elif topic == "transport":
        transport = info.get("transport", {})
        airport = transport.get("airport", "No data")
        roads = ", ".join(transport.get("roads", []))
        return f"🛣️ Transport: Airport - {airport}; Roads - {roads}"
    elif topic == "flora_fauna":
        flora_fauna = info.get("flora_fauna", {})
        animals = ", ".join(flora_fauna.get("common_animals", []))
        plants = ", ".join(flora_fauna.get("common_plants", []))
        return f"🦁 Flora & Fauna: Animals - {animals}; Plants - {plants}"
    elif topic == "traditional_dress":
        dress = info.get("traditional_dress", {})
        men = dress.get("men", "No data")
        women = dress.get("women", "No data")
        return f"👘 Traditional Dress: Men - {men}; Women - {women}"
    else:
        return f"📘 {topic.replace('_', ' ').title()}: {info.get(topic, 'No data')}"

def chatbot_response(message):
    state = find_state_in_message(message)
    if not state:
        return "❗ Please mention a valid state name."

    info = data[state]
    topics = extract_topics(message)
    message = message.lower()

    response = f"🗺️ {state} Info:\n"

    # If the user asked for full data
    if any(word in message for word in ["complete", "everything", "full", "all info", "all details"]):
        default_topics = list(info.keys())  # get all available topics
    elif not topics:
        default_topics = ["capital", "cities", "tourist_spots", "weather", "season", "food", "culture", "history"]
    else:
        default_topics = topics

    for topic in default_topics:
        response += format_topic_data(info, topic) + "\n"

    return response.strip()
