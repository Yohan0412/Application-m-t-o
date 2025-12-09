# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # ⬅️ Import nécessaire pour le CORS
import requests
from datetime import datetime

app = FastAPI()

# --- Configuration CORS ---
# ⚠️ Remplacez cette liste par l'URL de votre application React !
# Si vous utilisez Vite, c'est probablement http://localhost:5173
# Si vous utilisez create-react-app, c'est probablement http://localhost:3000
origins = [
     "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------------


weather_dict = {
    0: "Clair",
    1: "Partiellement nuageux",
    2: "Nuageux",
    3: "Couvert",
    45: "Brouillard",
    48: "Brouillard givrant",
    51: "Bruine légère",
    53: "Bruine modérée",
    55: "Bruine dense",
    61: "Pluie faible",
    63: "Pluie modérée",
    65: "Pluie forte",
    71: "Neige faible",
    73: "Neige modérée",
    75: "Neige forte",
    80: "Averses de pluie",
    81: "Averses modérées",
    82: "Averses fortes",
    95: "Orage",
    99: "Orage violent / grêle"
}


@app.get("/meteo")
def get_meteo():
    latitude = 44.558
    longitude = 6.077

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}&"
        f"daily=temperature_2m_max,temperature_2m_min,weathercode&"
        f"hourly=temperature_2m,precipitation_probability,precipitation&"
        f"current_weather=true&timezone=Europe/Paris"
    )

    response = requests.get(url)
    data = response.json()

    # Reformater proprement ce que tu veux renvoyer
    daily = []
    for i in range(len(data['daily']['time'])):
        daily.append({
            "date": data['daily']['time'][i],
            "t_max": data['daily']['temperature_2m_max'][i],
            "t_min": data['daily']['temperature_2m_min'][i],
            "weather": weather_dict.get(int(data['daily']['weathercode'][i]), "Code inconnu"),
            "returncodenumber": int(data['daily']['weathercode'][i]),
            
        })

    hourly = []
    for h in range(len(data['hourly']['time'])):
        date_obj = datetime.fromisoformat(data['hourly']['time'][h])
        hourly.append({
            "datetime": date_obj.strftime("%d/%m/%Y %H:%M"),
            "precipitation_probability": data['hourly']['precipitation_probability'][h]
        })

    return {
        "daily": daily,
        "hourly": hourly,
        "source": "open-meteo"
    }