import sys
import pandas as pd
from metar import Metar

from metar_str_cleansing import cleanse_metar_str


class CloudCondDescription:
    def __init__(self, dataset: pd.DataFrame):
        self.intensities = set()
        self.cloud_types = set()

        bad_rows = 0
        for metar_str in dataset["metar"]:
            metar_str = cleanse_metar_str(metar_str)

            try:
                metar = Metar.Metar(metar_str)

                for layer in metar.sky:
                    self.intensities.add(layer[0])
                    self.cloud_types.add(layer[2])

            except Metar.ParserError as e:
                bad_rows += 1

        print(bad_rows, "parser errors", file=sys.stderr)


