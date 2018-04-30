import lxml.html
from datetime import datetime
from datetime import timezone
import pandas as pd


# list of tuples: (airport, datetime, metar_str)
result_entries = []

airports = ["KATL", "KJFK", "KLAS"]  # Atlanta, JFK, Las Vegas

for airport in airports:
    for year in range(2012, 2017):
        print("starting year", year, "for airport", airport)
        for month in range(1, 13):
            filename = "data_html/{2}_{0:04d}_{1:02d}_metar.html".format(year, month, airport)

            root = lxml.html.parse(filename).getroot()

            strong_element = root.xpath('.//strong[contains(text(),"METAR/SPECI from")]')[0]
            table_element = strong_element.getparent().getparent()

            tr_elements_list = table_element.xpath('./tr')


            for tr_element in tr_elements_list:
                datetime_str = tr_element.getchildren()[1].text
                metar_str_with_redundant_whitespaces = tr_element.find(".//pre").text
                metar_str = ' '.join(metar_str_with_redundant_whitespaces.split())
                date = datetime.strptime(datetime_str, "%d/%m/%Y %H:%M->").replace(tzinfo=timezone.utc)

                result_entries.append((airport[1:], date, metar_str))


dataset = pd.DataFrame(result_entries, columns=["airport", "datetime", "metar"])

dataset.to_csv("metar_raw.csv", index=False)
