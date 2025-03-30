import google.generativeai as genai
from config import API_KEY

# Configure Gemini API
genai.configure(api_key=API_KEY)

def generate_travel_plan(destination, days, budget):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # AI Model
        prompt = f"""
        Create a {days}-day travel itinerary for {destination} within a budget of ${budget}.
        Include:
        - Day-wise plan with places to visit
        - Food options
        - Activities & estimated costs
        - Local travel options
        """
        response = model.generate_content(prompt)
        return response.text if response else "⚠️ Could not generate itinerary. Try again."
    except Exception as e:
        return f"❌ Error: {str(e)}"
import google.generativeai as genai
from config import API_KEY

# Configure Gemini API
genai.configure(api_key=API_KEY)

def generate_travel_plan(destination, days, budget, food_preference):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # AI Model
        prompt = f"""
        Create a {days}-day travel itinerary for {destination} within a budget of ₹{budget}.
        Include:
        - Day-wise plan with places to visit
        - Food options (Preference: {food_preference})
        - Activities & estimated costs
        - Local travel options
        - Hidden gems and budget-friendly tips
        """
        
        response = model.generate_content(prompt)
        
        return response.text if response else "⚠️ Could not generate itinerary. Try again."
    except Exception as e:
        return f"❌ Error: {str(e)}"
