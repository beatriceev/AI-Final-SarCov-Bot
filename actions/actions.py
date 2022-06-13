# This files contains your custom actions which can be used to run
# custom Python code.

# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from time import sleep
import json

class ActionGetReport(Action):

    def name(self) -> Text:
        return "action_get_report"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = next(tracker.get_latest_entity_values("place"), None)
        type = next(tracker.get_latest_entity_values("type"), None)
        print(f"{city}, {type}")
        with open("./covid_reports.json", "r+") as file:
            report = json.loads(file.read())

        if type == "cases":
            if not city:
                taiwan_total = report["Taiwan"]["Total cases"]
                taiwan_daily = report["Taiwan"]["Daily cases"].split("+")[1]
                taiwan_url = report["Taiwan"]["url"]
                msg = f"Our data is based in Taiwan. The total number of COVID cases is currently {taiwan_total} in Taiwan, including an increase of {taiwan_daily} cases today. You can also give me a specific city in Taiwan. For more details, check out the following link: {taiwan_url}."
                dispatcher.utter_message(text=msg)
                return []
            
            if city == "Hsinchu" or city == "Chiayi":
                city_name = city + " City"
                county_name = city + " County"
                city_url = report[city_name]["url"]
                county_url = report[county_name]["url"]
                total_city = report[city_name]["Total cases"]
                daily_city = report[city_name]["Daily cases"].split("+")[1]
                total_county = report[county_name]["Total cases"]
                daily_county = report[county_name]["Daily cases"].split("+")[1]
                msg = f"For {city_name}, the total number of COVID cases is currently {total_city} including an increase of {daily_city} cases today. Whereas for {county_name}, the total number of COVID cases is {total_county}, including an increase of {daily_county} cases today.\nFor more details, check out the following links:\n {city_name}: {city_url}\n {county_name}: {county_url}."
                dispatcher.utter_message(text=msg)
                return []
            
            if city not in report:
                msg = f"I don't recognize {city}. Is it spelled correctly?"
                dispatcher.utter_message(text=msg)
                return []
            
            total_in_city = report[city]["Total cases"]
            daily_in_city = report[city]["Daily cases"].split("+")[1]
            url_city = report[city]["url"]
            msg = f"The total number of COVID cases is currently {total_in_city} in {city}, including an increase of {daily_in_city} cases today. For more details, check out the following link: {url_city}."
            dispatcher.utter_message(text=msg)

            return []

        elif type == "deaths":
            taiwan_total = report["Taiwan"]["Total deaths"]
            taiwan_daily = report["Taiwan"]["Death cases"].split("+")[1]
            taiwan_url = report["Taiwan"]["url"]

            if city == "Taiwan":
                msg = f"The total number of deaths caused by COVID is currently {taiwan_total} in Taiwan, including an increase of {taiwan_daily} deaths this week. For more details, check out the following link: {taiwan_url}."
                dispatcher.utter_message(text=msg)
                return []

            msg = f"Our data is based in Taiwan. The total number of deaths caused by COVID is currently {taiwan_total} in Taiwan, including an increase of {taiwan_daily} deaths this week. For more details, check out the following link: {taiwan_url}."
            dispatcher.utter_message(text=msg)
            return []
        
        elif type == "vaccine":
            taiwan_total = report["Taiwan"]["Total vaccinated"]
            taiwan_daily = report["Taiwan"]["Daily vaccinated"].split("+")[1]
            taiwan_url = report["Taiwan"]["url"]

            if city == "Taiwan":
                msg = f"The total number of people who have received COVID-19 Vaccination is currently {taiwan_total} in Taiwan, including an increase of {taiwan_daily} people today. For more details, check out the following link: {taiwan_url}."
                dispatcher.utter_message(text=msg)
                return []

            msg = f"Our data is based in Taiwan. The total number of people who have received COVID-19 Vaccination is currently {taiwan_total} in Taiwan, including an increase of {taiwan_daily} people today. For more details, check out the following link: {taiwan_url}."
            dispatcher.utter_message(text=msg)
            return []