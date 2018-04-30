from typing import List
import re


def remove_equal_sign_at_the_end(metar_str: str) -> str:
    if metar_str.endswith("="):
        metar_str = metar_str[:-1]  # without '=' at the end
    return metar_str


def move_COR_statement(metar_str: str) -> str:
    words: List = metar_str.split()
    if words[1] == "COR":
        del words[1]
        words.insert(3, "COR")
        metar_str = " ".join(words)
    return metar_str


def replace_TEMPO_700(metar_str: str) -> str:
    if "TEMPO 700" in metar_str:
        metar_str = metar_str.replace("TEMPO 700", "TEMPO 0700")
    return metar_str


BAD_WS_RE = re.compile(r"WS\s+R(?=\d\d[RL])")
def replace_WS_R_with_WS_RWY(metar_str: str) -> str:
    metar_str = BAD_WS_RE.sub("WS RWY", metar_str)
    return metar_str



def cleanse_metar_str(metar_str: str) -> str:
    metar_str = remove_equal_sign_at_the_end(metar_str)
    metar_str = move_COR_statement(metar_str)
    metar_str = replace_TEMPO_700(metar_str)
    metar_str = replace_WS_R_with_WS_RWY(metar_str)
    return metar_str
