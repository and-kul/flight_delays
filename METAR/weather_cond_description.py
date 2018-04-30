import sys
import pandas as pd
from metar import Metar

from metar_str_cleansing import cleanse_metar_str


class WeatherCondDescription:
    def __init__(self, dataset: pd.DataFrame):
        self.weather_cond_set = set()

        bad_rows = 0
        for metar_str in dataset["metar"]:
            metar_str = cleanse_metar_str(metar_str)

            try:
                metar = Metar.Metar(metar_str)
                if metar.present_weather() != "":
                    current_conditions = metar.present_weather().split("; ")
                    for cond in current_conditions:
                        self.weather_cond_set.add(cond)

            except Metar.ParserError as e:
                bad_rows += 1

        print(bad_rows, "parser errors", file=sys.stderr)

        self.weather_cond_dict = dict()

        for idx, cond in enumerate(self.weather_cond_set):
            self.weather_cond_dict[cond] = idx

        self.total_conditions = len(self.weather_cond_set)
        print("possible weather conditions", self.total_conditions)


    def get_list_of_weather_cond_names(self):
        return list(self.weather_cond_set)

