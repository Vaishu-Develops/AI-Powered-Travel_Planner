import os
import streamlit as st
import requests
import google.generativeai as genai
from dotenv import load_dotenv  # Load environment variables

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("⚠️ GOOGLE_API_KEY is not set. Please check your .env file.")
else:
    genai.configure(api_key=API_KEY)

# Initialize Gemini Model
model = genai.GenerativeModel("gemini-1.5-pro")

# Function to generate travel options
def get_travel_options(source, destination, preferences, assistance, language):
    prompt = f"""
    You are an AI travel assistant. The user wants to travel from {source} to {destination}.
    Preferences: {preferences}
    Assistance needed: {assistance}
    Preferred language: {language}
    
    Provide travel options including car, bus, train, and flights with estimated costs.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {e}"

# Streamlit App UI
def main():
    st.title("🌍 AI-Powered Travel Planner 🚀")
    st.write("Find the best travel options between two locations!")

    # User Input
    source = st.text_input("Enter your source location:", placeholder="e.g., New York")
    destination = st.text_input("Enter your destination:", placeholder="e.g., Los Angeles")

    # Assistance Option
    assistance = st.selectbox("Do you need special assistance?", ["None", "Elderly Support", "Disability Assistance"])

    # Language Selection
    language = st.selectbox("Select your preferred language", ["English", "Spanish", "French", "German", "Chinese"])

    # Preferences
    preferences = st.text_input("Enter your travel preferences (e.g., budget, comfort, speed):", placeholder="e.g., budget-friendly")

    # Button to Generate Travel Options
    if st.button("🔍 Get Travel Options"):
        if source and destination and preferences:
            with st.spinner("🚀 Generating travel options..."):
                travel_options = get_travel_options(source, destination, preferences, assistance, language)
            
            st.subheader("🚆 Available Travel Options:")
            st.write(travel_options)
        else:
            st.warning("⚠️ Please fill in all fields!")

if __name__ == "__main__":
    main()
