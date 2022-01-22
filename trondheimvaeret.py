#!/usr/bin/python3

import xml.etree.ElementTree as ET
import datetime
import requests

# ↓ Remove when testing ↓

import tokens
import tweepy
from time import sleep

# Authenticate to Twitter
auth = tweepy.OAuthHandler(tokens.consumer_key, tokens.consumer_secret)
auth.set_access_token(tokens.access_token, tokens.access_token_secret)
api = tweepy.API(auth)

# ↑ Remove when testing ↑

yr_headers = {
    'User-Agent': '@trondheimvaeret github.com/lordolem/trondheimvaeret',
}

# 63.4245, 10.4174
yr_params = (
    ('lat', '63.4245'),
    ('lon', '10.4174'),
    ('altitude', '10'),
)


xml_headers = {
    'User-Agent': '@trondheimvaeret github.com/lordolem/trondheimvaeret',
}

print("Program started")

# Get the time for sunrise and sunset
def get_sunrise_sunset():
    # Format the date
    today = datetime.date.today()
    today_date = today.strftime("%Y-%m-%d")
    
    # Add the date to the params
    xml_params = (
        ('lat', '63.422'),
        ('lon', '10.412'),
        ('date', f'{today_date}'),
        ('offset', ' 01:00'),
    )

    # Get the data
    response = requests.get('https://api.met.no/weatherapi/sunrise/2.0', headers=xml_headers, params=xml_params)
    # Something make it readable https://docs.python.org/3/library/xml.etree.elementtree.html
    xml_tree = ET.fromstring(response.content)
    # Remove unwanted characters
    sunrise = xml_tree[1][0][5].attrib["time"].split("T")[1].split("+")[0]
    sunset = xml_tree[1][0][8].attrib["time"].split("T")[1].split("+")[0]
    
    return sunrise, sunset

# Convert the wind direction to abbreviation
def get_wind_dir(deg):
    deg = float(deg)
    if 337.5 > deg <= 22.5:
        return "N"
    elif 22.5 < deg <= 67.5:
        return "NØ"
    elif 67.5 < deg <= 112.5:
        return "Ø"
    elif 112.5 < deg <= 157.5:
        return "SØ"
    elif 157.5 < deg <= 202.5:
        return "S"
    elif 202.5 < deg <= 247.5:
        return "SV"
    elif 247.5 < deg <= 292.5:
        return "V"
    elif 292.5 < deg <= 337.5:
        return "NV"
    else:
        return "404"


# Get all the weather variables from YR
def get_weather():
    # Get time and dates
    current_date = datetime.date.today()
    current_hour = datetime.datetime.now().strftime("%H")
    # "2022-01-07T10:00:00Z"
    yr_date_format = f"{current_date}T{current_hour}:00:00Z"
    response = requests.get('https://api.met.no/weatherapi/locationforecast/2.0/', headers=yr_headers, params=yr_params)
    data = response.json()

    sunrise, sunset = get_sunrise_sunset()
    
    # Find correct index for timeseries. Most likely the first or second one but whatever.
    # Not included, because I am not sure if its correct or not.
    # for i in range(len(data["properties"]["timeseries"])):
    #     if data["properties"]["timeseries"][i]["time"] == yr_date_format:
    #         correct_index = i
    
    correct_index = 0
    
    base_path = data["properties"]["timeseries"][correct_index]["data"]
    base_path_instant = base_path["instant"]["details"]
    base_path_6_hours = base_path["next_6_hours"]["details"]
    
    temp = base_path_instant["air_temperature"]
    temp_high = base_path_6_hours["air_temperature_max"]
    temp_low = base_path_6_hours["air_temperature_min"]
    precipitation = base_path_6_hours["precipitation_amount"]
    precipitation_prob = base_path_6_hours["probability_of_precipitation"]
    wind_speed = base_path_instant["wind_speed"]
    wind_dir = get_wind_dir(base_path_instant["wind_from_direction"])
    
    return sunrise, sunset, temp, temp_high, temp_low, precipitation, precipitation_prob, wind_speed, wind_dir

# Find the best clock emoji for the current time
def get_clock_emoji(time):
    if time == "06:00" or time == "18:00":
        return "🕕"
    elif time == "10:00":
        return "🕙"
    elif time == "14:00":
        return "🕑"
    elif time == "21:00":
        return "🕘"
    elif time == "00:00":
        return "🕛"
    else:
        return "-"

# Make the tweet pretty 
def pretty(time):
    sunrise, sunset, temp, temp_high, temp_low, precipitation, precipitation_prob, wind_speed, wind_dir = get_weather()
    sunrise, sunset, temp, temp_high, temp_low, precipitation, precipitation_prob, wind_speed, wind_dir = str(sunrise), str(sunset), str(temp), str(temp_high), str(temp_low), str(precipitation), str(precipitation_prob), str(wind_speed), str(wind_dir)
    output = []
    output.append(f"📍 Akkurat nå er det {temp}°C i Trondheim!\n#TrondheimVaeret")
    output.append(f"💨 {wind_speed} m/s 🧭 {wind_dir}")
    output.append(f"🌧 {precipitation} mm")
    output.append("------")
    output.append(f"🔥 {temp_high}°C")
    output.append(f"❄️ {temp_low}°C")
    if time == "06:00":
        output.append("------")
        output.append(f"🌅 {sunrise}")
        output.append(f"🌇 {sunset}")
    output.append("------")
    output.append(f"{get_clock_emoji(time)} Oppdatert: {time}")
    output.append("📖 Kilde: YR")

    return "\n".join(output)

# ↓ Remove when testing ↓
# Main while function to keep the bot running
while True:
    now = datetime.datetime.now()
    time = now.strftime("%H:%M")
    runningtime = now.strftime("%H:%M:%S")
   
    print(f"Running: {runningtime}")

    if time == "06:00" or time == "10:00" or time == "14:00" or time == "18:00" or time == "21:00" or time == "00:00":
        api.update_status(pretty(time))
        print("Tweet published - Going to sleep for 360 seconds...")
        sleep(360)
    
    sleep(10)
