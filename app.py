import streamlit as st
import google.generativeai as genai
import requests
import time
from config import API_KEY, UNSPLASH_ACCESS_KEY, GOOGLE_PLACES_API_KEY

# Configure Gemini AI
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="AI Travel Planner", page_icon="🌍", layout="wide")

# Styling & Header
st.markdown("""
    <style>
        .title { font-size: 2.5em; font-weight: bold; color: #ff5733; text-align: center; }
    </style>
    <div class='title'>✈️ AI-Powered Travel Planner 🇮🇳</div>
""", unsafe_allow_html=True)

st.write("🌍 **Plan your dream trip with AI! Get real-time suggestions based on your budget & preferences.**")

# User Inputs
destination = st.text_input("🏔️ **Enter Destination:**")
days = st.number_input("📅 **Number of Days:**", min_value=1, max_value=30, step=1)
budget = st.number_input("💰 **Budget (INR ₹):**", min_value=5000, step=1000)

# Additional Preferences
purpose = st.selectbox("🎯 **Purpose of Trip:**", ["Relaxation", "Adventure", "Cultural", "Business", "Others"])
col1, col2 = st.columns(2)
with col1:
    accommodation = st.radio("🏨 **Accommodation Type:**", ["Budget", "Mid-range", "Luxury"])
    food_preference = st.radio("🍽 **Food Preference:**", ["Vegetarian", "Non-Vegetarian", "Vegan", "Jain"])
    dietary_restrictions = st.text_input("🍴 **Dietary Restrictions (if any, e.g., gluten-free, dairy-free):**")
with col2:
    travel_mode = st.selectbox("🚗 **Preferred Mode of Travel:**", ["Flight", "Train", "Bus", "Road Trip"])
    activity_type = st.multiselect("🎭 **Activity Interests:**", ["Adventure", "Relaxation", "Culture", "Shopping"])
season = st.selectbox("🌦 **Preferred Season for Travel:**", ["Summer", "Winter", "Monsoon", "Any"])
walking_tolerance = st.selectbox("🚶‍♂️ **Walking Tolerance:**", ["Low", "Moderate", "High"])

# Function to Fetch Images from Unsplash
def get_destination_image(destination):
    url = f"https://api.unsplash.com/search/photos?query={destination}&client_id={UNSPLASH_ACCESS_KEY}&per_page=1"
    response = requests.get(url).json()
    if response["results"]:
        return response["results"][0]["urls"]["regular"]
    return None

# Function to Fetch Top Places from Google Places API
def get_top_places(destination):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=top+attractions+in+{destination}&key={GOOGLE_PLACES_API_KEY}"
    response = requests.get(url).json()
    places = [place["name"] for place in response.get("results", [])[:5]]
    return places if places else ["No data available"]

# AI Itinerary Generator with detailed cost breakdown
def generate_travel_plan(destination, days, budget, accommodation, food_preference, travel_mode, activity_type, season, purpose, dietary_restrictions, walking_tolerance):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
        Generate a detailed {days}-day travel itinerary for {destination} within ₹{budget}.
        - Purpose: {purpose}
        - Accommodation: {accommodation}
        - Food: {food_preference}
        - Dietary Restrictions: {dietary_restrictions}
        - Travel Mode: {travel_mode}
        - Activities: {', '.join(activity_type)}
        - Best time to visit: {season}
        - Walking Tolerance: {walking_tolerance}
        Include must-visit places, hidden gems, cultural experiences, and local food suggestions.
        Provide an estimated cost breakdown for each activity, transport, and accommodation.
        """
        response = model.generate_content(prompt)
        return response.text if response else "⚠️ Could not generate itinerary. Try again."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Generate Itinerary Button
if st.button("🎒 Generate Itinerary"):
    if destination and days and budget:
        with st.spinner("🔍 AI is curating your perfect travel plan..."):
            time.sleep(2)
            itinerary = generate_travel_plan(destination, days, budget, accommodation, food_preference, travel_mode, activity_type, season, purpose, dietary_restrictions, walking_tolerance)
            image_url = get_destination_image(destination)
            top_places = get_top_places(destination)
        
        # Display Itinerary
        st.subheader(f"📍 {destination} - Your Travel Itinerary")
        if image_url:
            st.image(image_url, caption=f"Beautiful view of {destination}")
        st.write("🗺 **Top Attractions:**", ", ".join(top_places))
        with st.expander("📆 **Day-wise Plan:**"):
            st.write(itinerary)
        
        st.write("💰 **Estimated Budget Breakdown:**")
        st.progress(75)  # Example progress bar
    else:
        st.warning("⚠️ **Please fill in all the fields!**")
