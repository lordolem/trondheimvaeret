#!/usr/bin/env python3

import requests
import datetime
import xml.etree.ElementTree as ET

yr_headers = {
    'User-Agent': '@trondheimvaeret github.com/omfj/trondheimvaeret',
}

# 63.4245, 10.4174
yr_params = (
    ('lat', '63.4245'),
    ('lon', '10.4174'),
    ('altitude', '10'),
)

xml_headers = {
    'User-Agent': '@trondheimvaeret github.com/omfj/trondheimvaeret',
}

def get_data():
    yr_response = requests.get('https://api.met.no/weatherapi/locationforecast/2.0/', headers=yr_headers, params=yr_params)
    data = yr_response.json()

    correct_index = 0

    base_path = data["properties"]["timeseries"][correct_index]["data"]
    instant = base_path["instant"]["details"]
    one_hour = base_path["next_1_hours"]["details"]

    return base_path, instant, one_hour


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

    return str(sunrise), str(sunset)


def get_wind_dir():
    _, instant, _ = get_data()

    deg = float(instant["wind_from_direction"])
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

def get_emoji():
    # Get symbol code
    base_path, _, _ = get_data()

    symbol = base_path["next_1_hours"]["summary"]["symbol_code"]

    # If symbol code ends with "*_night/day/*", split at "_"
    if "_" in symbol:
        symbol = symbol.split("_")[0]

    # if symbol in [""]:
    #     return "🌪" # Tornado

    if symbol in ["clearsky"]:
        return "☀" # Sun
    elif symbol in ["fair"]:
        return "🌤" # Sun behind small cloud
    elif symbol in ["rainandthunder", "heavyrainandthunder", "heavyrainshowersandthunder", "lightrainandthunder", "lightrainshowersandthunder"]:
        return "⛈" # Cloud with lightning and rain
    elif symbol in ["partlycloudy"]:
        return "🌥" # Sun behind big cloud
    elif symbol in ["snowshowers", "rainshowers", "heavyrainshowers", "lightrain", "lightrainshowers", "lightsleetshowers"]:
        return "🌦" # Sun behind big cloud with rain
    elif symbol in ["lightssleetshowersandthunder", "rainshowersandthunder"]:
        return "🌦🌩" # Cloud with lightning
    elif symbol in ["snowshowersandthunder", "snowandthunder", "lightssnowshowersandthunder"]:
        return "🌨🌩"
    elif symbol in ["snow", "heavysnow", "heavysnowandthunder", "lightsnow", "lightsnowandthunder"]:
        return "🌨" # Cloud with snow
    elif symbol in ["heavyrain", "rain"]:
        return "🌧" # Cloud with rain
    elif symbol in ["cloudy"]:
        return "☁" # Normal cloud
    elif symbol in ["clearsky"]:
        return "🌙" # Moon
    elif symbol in ["fog"]:
        return "🌫" # Fog
    elif symbol in ["sleet", "heavysleet", "lightsleet", "heavysleetshowers", "heavysnowshowers", "heavysnowshowersandthunder"]:
        return "🌨🌧" # Snow and rain
    elif symbol in ["sleetshowersandthunder", "sleetshowers", "sleetandthunder", "heavysleetandthunder", "heavysleetshowersandthunder", "lightsleetandthunder"]:
        return "🌨🌧⚡" # Snow, rain and thunder
    else:
        return "☁"

def get_temp():
    _, instant, _ = get_data()
    return instant["air_temperature"]

def get_precipitation():
    _, _, one_hour = get_data()
    return one_hour["precipitation_amount_min"], one_hour["precipitation_amount_max"], one_hour["precipitation_amount"]

def get_wind_speed():
    _, instant, _ = get_data()
    return instant["wind_speed"]

def get_gust_speed():
    _, instant, _ = get_data()
    return instant["wind_speed_of_gust"]
