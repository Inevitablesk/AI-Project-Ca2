import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("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" )) 

# --- Add Dataset Validation Function Here ---
def validate_places(user_input):
    """Validate user input against dataset"""
    with open('backend/data/tourism_dataset.json') as f:  # Ensure correct path
        dataset = json.load(f)
    
    user_places = [p.strip().lower() for p in user_input.split(",")]
    valid_places = []
    
    for place in dataset:
        if place['Place_Name'].lower() in user_places:
            valid_places.append({
                'name': place['Place_Name'],
                'desc': place['Place_desc'],
                'category': place['Category']
            })
    
    return valid_places

# --- Original Model Setup ---
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [...]  # Keep your existing settings

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# --- Modified Main Logic ---
def is_trip_related(query):
    """Check if input is trip-related using AI"""
    prompt = f'''Is this query about travel/tourism? Answer ONLY YES/NO: "{query}"'''
    response = model.generate_content(prompt)
    return "YES" in response.text.upper()

# Get user inputs
x = input("Enter the number of days for your trip: ")
dest = input("Enter the places (comma-separated): ")

if not is_trip_related(dest):
    print("If you want to ask any information Except trip related Kindly go to Chat GPT, Google, Gemini, Perplexity, E.T.C, use me only for trip related guidance")
else:
    # --- Add Validation Check Here ---
    valid_places = validate_places(dest)
    if not valid_places:
        print("Error: No matching places found in our database!")
        exit()

    # --- Modified Prompt with Dataset Info ---
    prompt_parts = f'''Create a {x}-day itinerary using these verified places: {[p['name'] for p in valid_places}
Include:
1. Safe, beautiful places with moderate activities: {[p['desc'] for p in valid_places]}
2. Tourism Development Corporation contact details
3. 10 hotels sorted cheap to expensive with approximate prices
4. Transportation hierarchy (metro > Rapido > cabs)
    
Format output as JSON with these keys: Days, Contact, Hotels, Transportation'''

    response = model.generate_content(prompt_parts)

    # Save and display results
    with open("output.json", 'w') as json_file:
        json.dump(response.text, json_file)
    print(response.text)
