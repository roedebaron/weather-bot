from datetime import datetime, timedelta, timezone
from glob import glob
import discord
from src.models import WeatherForecast, WeatherForecastQuery

from src.dto_yr_data_complete import DataComplete, Timesery

import src.weather_client as weather_client
from src.utils import to_local_time


# local_time_zone_val = None

# Retrieves rainy forecast.


def get_forecast(query: WeatherForecastQuery):

    data: DataComplete = weather_client.get_forecast(query.lat, query.lon)

    # Convert to domain

    model = dto_to_model(data, query)

    return model


# XXX: Rette sted?
def dto_to_model(weather_data: DataComplete, query: WeatherForecastQuery) -> WeatherForecast:
    print(query.is_only_high_prob)
    # global local_time_zone_val

    # Get summary for next 12 hours
    symbol_code_12_h = weather_data.properties.timeseries[
        0].data.next_12__hours.summary.symbol_code or "No symbol code"

    updated_at_utc = weather_data.properties.meta.updated_at

    # Include only entries up to and including a certain date.
    date_limit = weather_data.properties.timeseries[0].time

    if(query.should_include_next_day):
        # If late, get entries for the next day also
        date_limit = date_limit + timedelta(days=1)
        # print("new date limit: " + str(date_limit))

        # Find 12h symbol for tomorrow morning # XXX: Evt. slå sammen med nedenstående
        symbol_code_12_h = next(
            (forecast.data.next_12__hours.summary.symbol_code for forecast in weather_data.properties.timeseries if forecast.time > query.next_day_summary_time_utc))

    # Get rainy hours i.e. contains any precipation
    rainy_forecasts: list[Timesery] = []
    for forecast in weather_data.properties.timeseries:  # XXX Ryk i funktion
        # Conditions: not exceeding date limit, has 1 hour summary data (some entries only have 6+12 hour forecast), has precipation
        next_hour_forecast = forecast.data.next_1__hours
        if next_hour_forecast and (forecast.time.date() <= date_limit.date()) and (next_hour_forecast.details.precipitation_amount_max > 0):
            rainy_forecasts.append(forecast)

    # Apply filter: Now get the hour_forecasts with rain in symbol (i.e. high prob of rain) ## Ryk i funktion, bool whether apply
    # Ignore not so rainy hours
    if query.is_only_high_prob:
        rainy_forecasts = [
            forecast for forecast in rainy_forecasts if "rain" in forecast.data.next_1__hours.summary.symbol_code]

    return WeatherForecast(rainy_forecasts, query.should_include_next_day, symbol_code_12_h, updated_at_utc)
