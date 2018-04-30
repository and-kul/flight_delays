import pandas as pd
from datetime import datetime

import sys
from metar import Metar
from typing import List
from metar_str_cleansing import cleanse_metar_str
from weather_cond_description import WeatherCondDescription


def from_sky_to_list_of_10_elements(sky: List) -> List:
    result = [0, 10000.0, 0, 0,
              0, 10000.0, 0, 0,
              0, 10000.0]

    from_intensity_to_number = {
        "CLR": 0,
        "NSC": 0,
        "FEW": 1,
        "SCT": 3,
        "BKN": 6,
        "OVC": 8
    }

    # todo: changing
    # if len(sky) == 1 and sky[0][0] in ["CLR", "NSC"]:
    if len(sky) > 0 and sky[0][0] in ["CLR", "NSC"]:
        return result

    # if len(sky) > 1 and sky[0][1].value("m") > sky[1][1].value("m"):
    #     print("handling")
    #     tmp = sky[0]
    #     sky[0] = sky[1]
    #     sky[1] = tmp


    # clouds_hidden
    if len(sky) == 1 and sky[0][0] == "VV":
        result[8] = 1
        result[9] = sky[0][1].value("m")
        return result

    if len(sky) > 0 and sky[0][0] != "CLR":
        result[0] = from_intensity_to_number[sky[0][0]]
        result[1] = sky[0][1].value("m")
        if sky[0][2] == "CB":
            result[2] = 1
        elif sky[0][2] == "TCU":
            result[3] = 1

    if len(sky) > 1 and sky[1][0] != "CLR":
        result[4] = from_intensity_to_number[sky[1][0]]
        result[5] = sky[1][1].value("m")
        if sky[1][2] == "CB":
            result[6] = 1
        elif sky[1][2] == "TCU":
            result[7] = 1

        if result[5] < result[1]:
            print("ALERT", file=sys.stderr)
            print(result[1], result[5], file=sys.stderr)


    return result









def from_metar_to_list_of_features(airport: str, timestamp: datetime, m: Metar.Metar) -> List:

    result = [
        airport,
        timestamp,
        m.code,

        m.mod,

        # m.station_id,

        m.wind_speed.value("mps") if m.wind_speed else None,
        m.wind_gust.value("mps") if m.wind_gust else None,


        m.wind_dir.value() if m.wind_dir else None,
        m.wind_dir_from.value() if m.wind_dir_from else None,
        m.wind_dir_to.value() if m.wind_dir_to else None,

        m.vis.value("m") if m.vis else None,

        m.max_vis.value("m") if m.max_vis else None,
        m.max_vis_dir.value() if m.max_vis_dir else None,

        m.runway[0][1].value("m") if m.runway else None,
        m.runway[0][2].value("m") if m.runway else None,


        m.temp.value("C") if m.temp else None,
        m.dewpt.value("C") if m.dewpt else None,
        m.press.value("HPA") if m.press else None,

        str(m.sky_conditions("; ")),

        # str(m.weather),
        str(m.present_weather()),
        # str(m.recent),

        # str(m.sky),
        # str(m.windshear),

        # str(m._trend),
        # str(m._trend_groups),
        # str(m._remarks),
        # str(m._unparsed_groups),
        # str(m._unparsed_remarks),

    ]
    return result


def get_bitmap_of_weather_conditions(m: Metar.Metar, weather_desc: WeatherCondDescription):
    bitmap = [0] * weather_desc.total_conditions

    if m.present_weather() != "":
        current_conditions = m.present_weather().split("; ")
        for cond in current_conditions:
            bitmap[weather_desc.weather_cond_dict[cond]] = 1

    return bitmap



column_names = [
    "airport",
    "timestamp",
    "code",

    "mod",
    # "station_id",

    "wind_speed_mps",
    "wind_gust_mps",


    "wind_dir",
    "wind_dir_from",
    "wind_dir_to",

    "vis",

    "additional_vis",
    "additional_vis_dir",

    "runway_visual_range_from",
    "runway_visual_range_to",

    "temp",
    "dewpt",
    "press",

    "sky_conditions",

    # "weather",
    "present_weather",
    # "recent",

    # "sky",
    # "windshear",

    # "_trend",
    # "_trend_groups",
    # "_remarks",
    # "_unparsed_groups",
    # "_unparsed_remarks",

]

column_names_cloud = [
    "first_layer_coverage",
    "first_layer_height",
    "first_layer_CB",
    "first_layer_TCU",
    "second_layer_coverage",
    "second_layer_height",
    "second_layer_CB",
    "second_layer_TCU",
    "clouds_hidden",
    "vertical_visibility"
]




dataset = pd.read_csv("metar_raw.csv")

weather_desc = WeatherCondDescription(dataset)



all_reports = []

for row in dataset.itertuples():
    metar_str = cleanse_metar_str(row.metar)
    timestamp = row.datetime
    airport = row.airport

    # metar = Metar.Metar(metar_str)
    # all_reports.append(from_metar_to_list_of_features(metar))

    try:
        metar = Metar.Metar(metar_str)
        if metar.mod == "NO DATA":
            continue
        current_report = from_metar_to_list_of_features(airport, timestamp, metar)
        current_report += from_sky_to_list_of_10_elements(metar.sky)
        current_report += get_bitmap_of_weather_conditions(metar, weather_desc)

        all_reports.append(current_report)
    except Metar.ParserError as e:
        # print("ParserError:", metar_str)
        # print(e)
        pass


print("Good", len(all_reports))
print("Bad", dataset.shape[0] - len(all_reports), file=sys.stderr)


table = pd.DataFrame(all_reports, columns=column_names + column_names_cloud + weather_desc.get_list_of_weather_cond_names())
print(table.shape)
table.to_csv("table.csv", index=False)
