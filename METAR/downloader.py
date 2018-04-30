import time
from calendar import monthrange
import os

import requests


airports = ["KATL", "KJFK", "KLAS"]  # Atlanta, JFK, Las Vegas

for airport in airports:
    for year in range(2012, 2017):
        for month in range(1, 13):
            parameters = {
                "lang": "en",
                "lugar": airport,  # ICAO ID
                "tipo": "ALL",  # all types of reports
                "ord": "DIR",  # chronological order
                "nil": "SI",  # include NIL reports
                "fmt": "html",  # result in html format

                "ano": str(year),  # year from
                "mes": str(month).zfill(2),  # month from
                "day": "01",  # day from
                "hora": "00",  # hour from

                "anof": str(year),  # year to
                "mesf": str(month).zfill(2),  # month to
                "dayf": str(monthrange(year, month)[1]),  # day to
                "horaf": "23",  # hour to
                "minf": "59",  # minutes to

                "send": "send"  # ???
            }

            filename = "data_html/{2}_{0:04d}_{1:02d}_metar.html".format(year, month, airport)

            if os.path.exists(filename):
                print(filename, "already exists, continuing...")
                continue

            while True:
                try:
                    response = requests.get("https://www.ogimet.com/display_metars2.php", params=parameters)

                    # rate limit is not exceeded
                    if len(response.text) > 10000:

                        with open(filename, "w", encoding="utf-8") as file:
                            file.write(response.text)
                            print("ok", filename)
                        time.sleep(180)  # wait for 180 seconds
                        break
                    else:
                        print("error: rate limit exceeded, waiting for 15 seconds...")
                        time.sleep(15)  # wait for 15 seconds
                except Exception as e:
                    print(e, "waiting for 5 sec...")
                    time.sleep(5)
