import requests
from datetime import datetime


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
data = response.json()  # <- important !


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

print("Prévisions météo à Gap pour les prochains jours :")
for i in range(len(data['daily']['time'])):
    date = data['daily']['time'][i]
    date_str = data['daily']['time'][i]    
    t_max = data['daily']['temperature_2m_max'][i]
    t_min = data['daily']['temperature_2m_min'][i]
    weather_code = data['daily']['weathercode'][i]
    weather_codelettre = weather_dict.get(int(weather_code), "Code inconnu")
    print(f"{date} → Max: {t_max}°C, Min: {t_min}°C, {weather_codelettre}")
    
    
for h in range(len(data['hourly']['time'])):
     # Récupère la date brute en ISO8601
    date_iso = data['hourly']['time'][h]

    # Convertit l'ISO8601 en datetime
    date_obj = datetime.fromisoformat(date_iso)

    # Reformate en quelque chose de lisible
    date_lisible = date_obj.strftime("%d/%m/%Y %H:%M")   
    precipitation = data['hourly']['precipitation_probability'][h]
    weather_codelettre = weather_dict.get(int(weather_code), "Code inconnu")
    print(f" date: {date_lisible} précipitation en % :{precipitation}")
    
    