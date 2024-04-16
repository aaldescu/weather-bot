import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import pytz
from timezonefinder import TimezoneFinder

# Load environment variables
load_dotenv()

def get_weather_forecast(api_key, lat, lon):
    # Update the URL if necessary to reflect the correct API version and parameters
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely&units=metric&appid={api_key}"
    response = requests.get(url)
    return response.json()

def analyze_weather(forecast, local_timezone):
    suitable_times = []
    dry_times = []
    today = datetime.now(pytz.utc).astimezone(local_timezone).date()
    next_weekend = today + timedelta(days=(5 - today.weekday() + 7) % 7)  # Next Saturday

    # Printing the time interval of forecast data
    print(f"Analyzing forecast data from {today} to {next_weekend + timedelta(days=1)}")

    for hour in forecast['hourly']:
        hour_time = datetime.fromtimestamp(hour['dt'], pytz.utc).astimezone(local_timezone)
        if today < hour_time.date() <= next_weekend + timedelta(days=1):
            rain_chance = hour.get('pop', 0) * 100  # Probability of precipitation
            # Check if weather conditions are suitable for drying
            if hour['weather'][0]['main'] == 'Clear' and \
               hour['temp'] > 15 and \
               hour['humidity'] < 60 and rain_chance < 20:
                suitable_times.append(hour_time.strftime('%A, %B %d at %H:%M'))
            # Collect data for dry times sorting by humidity and rain chance
            dry_times.append({
                'time': hour_time.strftime('%A, %B %d at %H:%M'),
                'temp': hour['temp'],
                'humidity': hour['humidity'],
                'clouds': hour['clouds'],
                'rain_chance': rain_chance
            })

    # If no suitable times found, sort by a combination of humidity and rain chance
    if not suitable_times:
        dry_times.sort(key=lambda x: (x['rain_chance'], x['humidity'] ))
        #return dry_times[:3], False
        return dry_times, False

    return suitable_times, True

def main():
    API_KEY = os.getenv('API_KEY')
    # Coordinates for Frankfurt am Main, Germany
    latitude = 50.1109
    longitude = 8.6821
    
    # Determine the timezone from latitude and longitude
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lat=latitude, lng=longitude)
    if timezone_str is None:
        print("Timezone could not be determined.")
        return
    timezone = pytz.timezone(timezone_str)
    
    forecast = get_weather_forecast(API_KEY, latitude, longitude)
    result, is_suitable = analyze_weather(forecast, timezone)
    
    if is_suitable:
        print("Good times to dry clothes outdoors:")
        for time in result:
            print(time)
    else:
        print("No suitable times for drying clothes outdoors found. Top 3 driest times are:")
        for time_info in result:
            print(f"{time_info['time']}: Temp={time_info['temp']}°C, Humidity={time_info['humidity']}%, Clouds={time_info['clouds']}%, Rain Chance={time_info['rain_chance']}%")

if __name__ == "__main__":
    main()
