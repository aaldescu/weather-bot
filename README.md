# Outdoor Clothes Drying Assistant
When is the best time to do sports outside or dry clothes

This Python script utilizes the OpenWeatherMap API to determine the optimal times for drying clothes outdoors based on weather conditions such as humidity, temperature, wind speed, and rain chances. It focuses on finding the best times within a forecast period up to the next weekend and provides fallback suggestions if no ideal conditions are found.

## Features

- **Weather Analysis**: Identifies clear, warm, breezy, and dry hours suitable for drying clothes outdoors.
- **Fallback Suggestions**: Offers the top 3 driest times based on minimal humidity and rain chances if no ideal drying times are found.
- **Dynamic Timezone Handling**: Automatically adjusts for the timezone based on the provided latitude and longitude.

## Setup

### Prerequisites

You need Python 3.x and pip installed on your system. Additionally, you will need an API key from OpenWeatherMap, which you can obtain by signing up at their website.

### Dependencies

Install the required Python packages using pip:
```bash
pip install requests pytz timezonefinder python-dotenv
```

## Configuration
Clone or download this repository to your local machine.

Create a .env file in the root directory of the project and add your OpenWeatherMap API key like this:
```bash
API_KEY=your_openweathermap_api_key_here
```
Ensure you have internet access for the API calls.

## Usage
To run the script, navigate to the script's directory in your terminal and execute:

```bash
python clothes_drying_assistant.py
```

The script will output the best times for drying clothes or the top 3 alternative times based on weather conditions.

## Customization
- **Location**: Set the latitude and longitude variables in the main function to the coordinates of your desired location.
- **Adjusting Parameters**: Modify the conditions in the analyze_weather function if you wish to change what is considered suitable weather for drying clothes.

## Notes
The script currently handles the forecast for up to the next weekend from the current date.
Ensure that your API key is kept confidential and is not exposed in shared or public environments.

## Support
For support, contact the email linked with this account or open an issue in the repository if applicable.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

