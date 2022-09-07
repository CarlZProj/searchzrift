import os

RIOT_API_KEY = os.environ.get('RIOT_API_KEY')
RIOT_API_KEY_HEADER = {"X-Riot-Token": RIOT_API_KEY}

AMERICAS = "americas"
EUROPE = "europe"
ASIA = "asia"

server_to_region_map = {
    "na1": AMERICAS,
    "br1": AMERICAS,
    "eun1": EUROPE,
    "euw1": EUROPE,
    "la1": AMERICAS,
    "la2": AMERICAS,
    "na1": AMERICAS,
    "oc1": AMERICAS,
    "ru": EUROPE,
    "tr1": EUROPE,
    "jp1": ASIA,
    "kr": ASIA,
}

S12_AMERICAS_START_TIME = 1641549600
S12_EUROPE_START_TIME = 1641614400
S12_ASIA_START_TIME = 1641499200

region_to_season_12_start_time_map = {
    AMERICAS: S12_AMERICAS_START_TIME,
    EUROPE: S12_EUROPE_START_TIME,
    ASIA: S12_ASIA_START_TIME,
}

MAX_MATCH_IDS = 100

"""
team_position_to_match_rating_ratios_map = {
    "TOP": {
        "overall": 0.1,
        "participation": 0.1,
        "offense": 0.2,
        "defense": 0.1,
        "objectives_and_turrets": 0.2,
        "income": 0.2,
        "vision": 0.05,
        "utility": 0.05,
        
    }, 
    "JUNGLE": {
        "overall": 0.1,
        "participation": 0.2,
        "offense": 0.15,
        "defense": 0.1,
        "objectives_and_turrets": 0.2,
        "income": 0.1,
        "vision": 0.1,
        "utility": 0.05,
    },
    "MIDDLE": {
        "overall": 0.1,
        "participation": 0.2,
        "offense": 0.3,
        "defense": 0.05,
        "objectives_and_turrets": 0.05,
        "income": 0.2,
        "vision": 0.05,
        "utility": 0.05, 
    },
    "BOTTOM": {
        "overall": 0.1,
        "participation": 0.1,
        "offense": 0.25,
        "defense": 0.05,
        "objectives_and_turrets": 0.1,
        "income": 0.30,
        "vision": 0.05,
        "utility": 0.05,
    },
    "UTILITY" : {
        "overall": 0.1,
        "participation": 0.3,
        "offense": 0.1,
        "defense": 0.1,
        "objectives_and_turrets": 0.05,
        "income": 0.05,
        "vision": 0.2,
        "utility": 0.1,
    },
    "": {
        "overall": 0.1,
        "participation": 0.3,
        "offense": 0.1,
        "defense": 0.1,
        "objectives_and_turrets": 0.1,
        "income": 0.1,
        "vision": 0.1,
        "utility": 0.1,
    },
}
"""