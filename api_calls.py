from pyodide.http import pyfetch
import asyncio
from datetime import date
import numpy as np

async def get_city_coord(city_name):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"
    response = await pyfetch(url=url, method="GET")
    result = await response.json()
    result = result["results"][0]
    return {"lat": result["latitude"], "long": result["longitude"]}

async def get_today_temperature(coord):
    today = date.today()
    url = f'https://api.open-meteo.com/v1/forecast?'
    url += f'latitude={coord["lat"]}&'
    url += f'longitude={coord["long"]}&'
    url += f'hourly=temperature_2m&'
    url += f'start_date={today.strftime("%Y-%m-%d")}&'
    url += f'end_date={today.strftime("%Y-%m-%d")}'   

    response = await pyfetch(url=url, method="GET")
    result = await response.json()
    temperature = round(np.mean(result["hourly"]["temperature_2m"]), 1)
    return temperature

def solution_to_json(solution):
    result = {}
    for i, dress in enumerate(solution):
        piece = body_parts[i][dress]
        result[class_names[i]] = piece.name
    return result
