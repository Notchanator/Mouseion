"""Animal theme — 16 card definitions (one per pair).

A theme is a flat list of 16 dicts. Each entry describes a pair; the game deals
two cards from each entry. To add a new theme, drop a sibling module here with
its own list of 16 entries and a matching asset folder under
``frontend/assets/themes/<name>/``.
"""

ANIMAL_THEME = [
    {"id": 1,  "name": "Fox",      "color": "#E86B3A", "image": "fox.png",      "text": "Clever & quick"},
    {"id": 2,  "name": "Whale",    "color": "#3A7BE8", "image": "whale.png",    "text": "Deep & wise"},
    {"id": 3,  "name": "Owl",      "color": "#8C6D46", "image": "owl.png",      "text": "Watchful at night"},
    {"id": 4,  "name": "Rabbit",   "color": "#D98CB3", "image": "rabbit.png",   "text": "Soft & swift"},
    {"id": 5,  "name": "Bear",     "color": "#7A5230", "image": "bear.png",     "text": "Strong & calm"},
    {"id": 6,  "name": "Frog",     "color": "#4FB05A", "image": "frog.png",     "text": "Leaps & sings"},
    {"id": 7,  "name": "Deer",     "color": "#B5895A", "image": "deer.png",     "text": "Gentle wanderer"},
    {"id": 8,  "name": "Otter",    "color": "#6FA8A0", "image": "otter.png",    "text": "Playful swimmer"},
    {"id": 9,  "name": "Hedgehog", "color": "#9B7B53", "image": "hedgehog.png", "text": "Small & spiky"},
    {"id": 10, "name": "Wolf",     "color": "#6B7280", "image": "wolf.png",     "text": "Loyal to the pack"},
    {"id": 11, "name": "Penguin",  "color": "#2C3E50", "image": "penguin.png",  "text": "Cool & dapper"},
    {"id": 12, "name": "Tiger",    "color": "#E8943A", "image": "tiger.png",    "text": "Fierce & striped"},
    {"id": 13, "name": "Koala",    "color": "#9AA5AD", "image": "koala.png",    "text": "Sleepy climber"},
    {"id": 14, "name": "Hawk",     "color": "#A0522D", "image": "hawk.png",     "text": "Keen-eyed flyer"},
    {"id": 15, "name": "Seal",     "color": "#5B8DAE", "image": "seal.png",     "text": "Sleek & curious"},
    {"id": 16, "name": "Lynx",     "color": "#C2884E", "image": "lynx.png",     "text": "Silent hunter"},
]
