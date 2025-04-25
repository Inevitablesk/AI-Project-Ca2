import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("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"))

# Dataset validation functions
def validate_places(user_input, dataset_path="tourism_dataset.json"):
    with open(dataset_path) as f:
        places_data = json.load(f)
    valid_places = []
    for place in user_input.split(","):
        place = place.strip()
        if any(p["Place_Name"].lower() == place.lower() for p in places_data):
            valid_places.append(place)
    return valid_places

def get_dataset_details(valid_places):
    with open("tourism_dataset.json") as f:
        dataset = json.load(f)
    details = []
    for place_name in valid_places:
        found = next((p for p in dataset if p["Place_Name"].lower() == place_name.lower()), None)
        if found:
            details.append(f"{found['Place_Name']} ({found['Category']}): {found['Place_desc']}")
    return "\n".join(details)

# Model configuration
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
]

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Main logic
def is_trip_related(query):
    prompt = f'''Is this query about travel/tourism? Answer ONLY YES/NO: "{query}"'''
    response = model.generate_content(prompt)
    return "YES" in response.text.upper()

# Get user inputs
x = input("Enter the number of days for your trip: ")
dest = input("Enter places (comma-separated): ")
people = input("Number of travelers: ")
start_date = input("Start date (YYYY-MM-DD): ")

if not is_trip_related(dest):
    print("If you want to ask any information except trip related, kindly go to Chat GPT, Google, Gemini, Perplexity, etc. Use me only for trip related guidance.")
else:
    valid_places = validate_places(dest)
    if not valid_places:
        print("Error: No matching places found in our database!")
        exit()

    dataset_details = get_dataset_details(valid_places)

    prompt_parts = f'''Create a {x}-day itinerary for {valid_places} starting {start_date}. 
Consider:
- Verified place details: {dataset_details}
- Travel group size: {people} people
Include:
1. Hour-by-hour daily schedule with realistic travel times
2. 5 budget & 5 luxury hotel options with prices
3. Transportation modes between locations (metro > Rapido > cab priority)
4. Total cost estimate breakdown
Format output as JSON with keys: days, hotels, transport, costs'''

    response = model.generate_content(prompt_parts)

    # Save and display results
    with open("output.json", 'w') as json_file:
        json.dump(json.loads(response.text), json_file, indent=2)
    print(response.text)
