import requests
from requests.exceptions import RequestException
import time

API_KEY = "BQGPUW9HYTACK9GUGMCWBNFE5"  # register on https://www.visualcrossing.com/ to get API_KEY


def retry(func):
    def wrapper_retry(*args, **kwargs):
        retries = [5, 30]
        for seconds in retries:
            try:
                return func(*args, **kwargs)
            except RequestException:
                print(f"Failed to get data. Retrying in {seconds} seconds")
                time.sleep(seconds)
        return func(*args, **kwargs)

    return wrapper_retry


@retry
def get_weather_by_day_from_api(*, date: str, city: str) -> dict:
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{date}/{date}?unitGroup=us&key={API_KEY}"
    response = requests.get(url)
    weather_by_days = response.json()["days"]
    weather_by_day = weather_by_days[0]
    return weather_by_day


def fahrenheit_to_celsius(*, fahrenheit_temperature: float) -> int:
    return round((fahrenheit_temperature - 32) * 5 / 9)


def get_dangerous_hours(*, weather_by_hour: list[dict]) -> list[dict]:
    dangerous_hours = []
    for weather in weather_by_hour:
        uvindex = weather["uvindex"]
        time = weather["datetime"]
        celsius_temperature = fahrenheit_to_celsius(fahrenheit_temperature=weather["temp"])
        if uvindex >= 3:
            dangerous_hours.append({"time": time, "uvindex": uvindex, "temperature": celsius_temperature})

    return dangerous_hours


def get_simple_weather_forecast(*, weather_by_day: dict) -> dict:
    max_day_temperature = fahrenheit_to_celsius(fahrenheit_temperature=weather_by_day["tempmax"])
    min_night_temperature = fahrenheit_to_celsius(fahrenheit_temperature=weather_by_day["tempmin"])
    pressure = weather_by_day["pressure"]

    return {
        "max_day_temperature": max_day_temperature,
        "min_night_temperature": min_night_temperature,
        "pressure": pressure,
    }


date = "2025-08-21"
city = "Perm,RU"

weather_by_day = get_weather_by_day_from_api(date=date, city=city)
forecast = get_simple_weather_forecast(weather_by_day=weather_by_day)

print(f"Максимальная температура днём: {forecast['max_day_temperature']} °C")
print(f"Минимальная температура ночью: {forecast['min_night_temperature']} °C")
print(f"Давление: {forecast['pressure']}")