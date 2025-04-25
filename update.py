import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("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" ))  # Use a valid API key

# Model configuration (unchanged)
generation_config = { ... }
safety_settings = [ ... ]
model = genai.GenerativeModel(...)

def is_trip_related(query):
    """Use AI to check if the input is trip-related."""
    prompt = f'''Is the following input related to travel, tourism, or trip planning? 
    Answer ONLY 'YES' or 'NO'. Input: "{query}"'''
    response = model.generate_content(prompt)
    return "YES" in response.text.upper()

# Get user inputs
days = input("Enter the number of days for your trip: ")
dest = input("Enter the places you want to visit: ")

# Check if input is trip-related
if not is_trip_related(dest):
    print("If you want to ask any information except trip-related, kindly go to Chat GPT, Google, Gemini, Perplexity, etc. Use me only for trip-related guidance.")
else:
    # Enhanced prompt for itinerary, hotels, and transport
    prompt = f'''
    Create a {days}-day itinerary for {dest}. Include:
    1. Safe and beautiful places with moderate activities.
    2. Contact details of the local Tourism Development Corporation.
    3. A list of 10 hotels sorted from cheap to expensive (include approximate prices).
    4. Transportation suggestions (prioritize metro if available, then Rapido, then cabs).
    
    Format the output as JSON with keys: Days, Contact, Hotels, Transportation.
    '''
    
    response = model.generate_content(prompt)
    
    # Save and print response
    with open("output.json", "w") as f:
        json.dump(response.text, f)
    print(response.text)
