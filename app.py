import streamlit as st
import requests
from datetime import datetime, timedelta
import pytz
from timezonefinder import TimezoneFinder
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
API_KEY = os.getenv('API_KEY')

def get_weather_forecast(lat, lon):
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely&units=metric&appid={API_KEY}"
    response = requests.get(url)
    return response.json()

def analyze_weather(forecast, local_timezone):
    dry_times = []
    today = datetime.now(pytz.utc).astimezone(local_timezone).date()
    next_weekend = today + timedelta(days=(5 - today.weekday() + 7) % 7)  # Next Saturday

    for hour in forecast['hourly']:
        hour_time = datetime.fromtimestamp(hour['dt'], pytz.utc).astimezone(local_timezone)
        if today < hour_time.date() <= next_weekend + timedelta(days=1):
            rain_chance = hour.get('pop', 0) * 100  # Probability of precipitation
            dry_times.append({
                'Time': hour_time.strftime('%A, %B %d at %H:%M'),
                'Temperature (°C)': hour['temp'],
                'Humidity (%)': hour['humidity'],
                'Clouds (%)': hour['clouds'],
                'Rain Chance (%)': rain_chance
            })

    # Inverting the sort order to prioritize lower rain chances first, then lower humidity
    dry_times.sort(key=lambda x: (x['Rain Chance (%)'], x['Humidity (%)']))
    return dry_times[:3]

def main():
    st.title("Outdoor Clothes Drying Assistant")
    lat = st.number_input("Enter Latitude:", format="%.4f")
    lon = st.number_input("Enter Longitude:", format="%.4f")
    if st.button("Analyze Weather"):
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lat=lat, lng=lon)
        if timezone_str:
            timezone = pytz.timezone(timezone_str)
            forecast = get_weather_forecast(lat, lon)
            results = analyze_weather(forecast, timezone)
            df = pd.DataFrame(results)
            st.write("Here are the top 3 best times for drying clothes outdoors:")
            st.table(df)
        else:
            st.error("Could not determine the timezone. Please check the latitude and longitude and try again.")

if __name__ == "__main__":
    main()
