#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, date
from colorama import Fore, Back, Style
import json, os, requests

# ONLY CHANGE THIS!

# =================
OBJECT_ID = "413"
# =================

# Settings
TEMPLATE_URL = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=OBJECTID={id}&outFields=cases,deaths,cases_per_population,last_update,cases7_per_100k,cases7_bl,death7_lk,cases7_per_100k_txt,cases_per_100k,cases7_lk,recovered,cases7_bl_per_100k,GEN,BEZ&returnGeometry=false&outSR=&f=json"

PATH_TO_CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache.json")

COLORS = [[50, "RED"], [10, "LIGHTYELLOW_EX"], [35, "LIGHTRED_EX"], [5, "GREEN"]]


def bubbleSort(arr):
    n = len(arr)

    # Traverse through all array elements
    for i in range(n - 1):

        # Last i elements are already in place
        for j in range(0, n - i - 1):

            if arr[j][0] > arr[j + 1][0]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr


class Cache:
    def __init__(self, CACHE_PATH):
        self.CACHE_PATH = CACHE_PATH

    # Save data in cache file.
    def save_cache(self, data):
        with open(self.CACHE_PATH, "w") as cache_file:
            json.dump(data, cache_file)

    # Read data from cache file
    def read_cache(self):
        with open(self.CACHE_PATH, "r") as cache_file:
            cache_data = json.loads(cache_file.read())

        return cache_data


class Incidence:
    def __init__(self, id, PATH_TO_CACHE, URL, THRESHOLDS):
        self.Cache = Cache(PATH_TO_CACHE)
        self.url = self.build_url(URL, id)
        self.thresholds = THRESHOLDS

    # Build request url.
    def build_url(self, template_url, id):
        if type(id) == type(str()) and id != "":
            return template_url.format(id=id)

        else:
            quit("Error in OBJECT_ID")

    # Get data from API.
    def get_data(self):
        # Data from API
        request = requests.get(self.url)

        if request.status_code == 200:
            data = request.json()

        else:
            quit("Error in Request")

        # Modify data
        data = data["features"][0]["attributes"]

        # Modify date
        old_data = data["last_update"]

        datetime_object = datetime.strptime(old_data, "%d.%m.%Y, %M:%H Uhr")

        new_date = datetime.strftime(datetime_object, "%Y-%m-%d")

        data["last_update"] = new_date

        # Save data into cache.
        self.Cache.save_cache(data)

        return data

    def load_data(self):
        # Read cache data
        try:
            cache = self.Cache.read_cache()

        # Get data from API and save in cache
        except FileNotFoundError:
            cache = self.get_data()

        try:
            # Check last update
            if cache["last_update"] == str(date.today()):
                # Data from cache
                data = cache

            else:
                # Data from API
                data = self.get_data()

        except:
            # Data from API
            data = self.get_data()

        return data

    def get_color(self, cases_per_100k):
        thresholds = bubbleSort(self.thresholds)

        # Convert string to float
        cases_per_100k = float(cases_per_100k)

        # Traverse through all array elements
        for i in range(len(thresholds)):
            # Check first element.
            if i == 0:
                if cases_per_100k < thresholds[i][0]:
                    return thresholds[i][1]

            # Check last element.
            if i == len(thresholds) - 1:
                if cases_per_100k > thresholds[i][0]:
                    return thresholds[i][1]

            if (
                cases_per_100k >= thresholds[i][0]
                and cases_per_100k < thresholds[i + 1][0]
            ):
                return thresholds[i][1]

    def show_data(self, data):
        # Covid data
        cases_per_100k = data["cases7_per_100k_txt"]
        cases_per_100k_bl = data["cases7_bl_per_100k"]
        total_cases, total_deaths = data["cases"], data["deaths"]

        # Color
        color_name = self.get_color(data["cases7_per_100k"])
        color = getattr(Back, color_name)

        # Metadata
        location, bezirk, date = data["GEN"], data["BEZ"], data["last_update"]
        source = "RKI"

        print(
            Style.BRIGHT
            + f"{bezirk} {location}\n\n"
            + Style.RESET_ALL
            + f"7-Tages-Inzidenz auf 100T Einwohner\n\n"
            + Style.BRIGHT
            + color
            + "   "
            + Back.RESET
            + " "
            + f"{cases_per_100k}"
            + Back.RESET
            + Style.RESET_ALL
            + "\n"
        )

        print(
            Style.DIM
            + f"Weitere Informationen\n"
            + f"Gesamt Fälle: {total_cases}\n"
            + f"Gesamt Tote: {total_deaths}\n"
            + f"Bundesland Inzidenz: {cases_per_100k_bl}\n"
            + f"Quelle: {source}, Stand: {date}"
            + Style.RESET_ALL
        )


def main():
    incidence = Incidence(OBJECT_ID, PATH_TO_CACHE, TEMPLATE_URL, COLORS)
    data = incidence.load_data()
    incidence.show_data(data)

if __name__ == '__main__':
    main()
