import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("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")) 

# Set up the model (keep original config)
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  }
]

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

def is_trip_related(query):
    """Check if input is trip-related using AI"""
    prompt = f'''Is this query about travel/tourism? Answer ONLY YES/NO: "{query}"'''
    response = model.generate_content(prompt)
    return "YES" in response.text.upper()

# Get user inputs
x = input("Enter the number of days for your trip : ")
dest = input("Enter the places you want to visit : ")

# Handle non-trip queries
if not is_trip_related(dest):
    print("If you want to ask any information Except trip related Kindly go to Chat GPT, Google, Gemini, Perplexity, E.T.C, use me only for trip related guidance")
else:
    # Enhanced prompt with hotels and transportation
    prompt_parts = f'''Create a {x}-day itinerary for {dest}. Include:
    1. Safe, beautiful places with moderate activities
    2. Tourism Development Corporation contact details
    3. 10 hotels sorted cheap to expensive with approximate prices
    4. Transportation hierarchy (metro > Rapido > cabs)
    
    Format output as JSON with these keys: Days, Contact, Hotels, Transportation'''

    response = model.generate_content(prompt_parts)

    # Save and display results
    with open("output.json", 'w') as json_file:
        json.dump(response.text, json_file)
    print(response.text)
