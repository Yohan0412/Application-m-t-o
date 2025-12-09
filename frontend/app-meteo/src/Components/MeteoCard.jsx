import Lottie from 'lottie-react';
import React, { useState, useEffect } from 'react';
import Cloudy from '../lottie/Cloudy.json';
import Foggy from "../lottie/Foggy.json";
import Sun from "../lottie/Sun.json";
import Fog from "../lottie/Fog.json";
import Rain from "../lottie/Rain.json";
import Snow from "../lottie/Snow.json";
import Thunderstorm from "../lottie/Thunderstorm.json"

const LOTTIES_MAPPING = {
  0: Sun,
  1: Foggy,
  2: Cloudy,
  3: Cloudy,
  45: Fog,
  48: Fog,
  51: Fog,
  53: Fog,
  55: Fog,
  61: Rain,
  63: Rain,
  65: Rain,
  71: Snow,
  73: Snow,
  75: Snow,
  80: Rain,
  81: Rain,
  82: Rain,
  95: Thunderstorm,
  99: Thunderstorm,

}

function MeteoCard() {
  const [meteoData, setMeteoData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [lottiePath, setLottiePath] = useState(null)

  useEffect(() => {
    const apiUrl = 'http://localhost:8000/meteo'; 

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`Erreur HTTP: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        setMeteoData(data.daily[0]); // On prend les données du jour 1
        
        // 1. Récupérer le code météo du Back-end
        const code = data.daily[0].returncodenumber; // Assurez-vous que FastAPI renvoie 'weather_code'
        
        // 2. Trouver le chemin Lottie correspondant
        const path = LOTTIES_MAPPING[code] || null;
        setLottiePath(path); 
      })
      .catch(error => {
        console.error("Échec de la liaison back-front:", error);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []); 

  if (loading) {
    return <div>Chargement des données météo...</div>;
  }

  if (!meteoData) {
    return <div>Erreur lors de la connexion au back-end.</div>;
  }
  // 3. Afficher les données récupérées du back-end
  return (
    <div style={{ textAlign: 'center', padding: '20px' }}>
      <h1>Météo du Jour</h1>

      {lottiePath ? (
        <div style={{ width: '150px', height: '150px', margin: '20px auto' }}>
          <Lottie
            // Le chemin/URL (lottiePath) est utilisé ici comme 'animationData'
            animationData={lottiePath} 
            loop={true}
            autoplay={true}
          />
        </div>
      ) : (
        <p>Icône non disponible pour le code : {meteoData.returncodenumber}</p>
      )}

      <p>Température Max (Aujourd'hui): **{meteoData.t_max}°C**</p>
      <p>État: {meteoData.weather}</p>
    </div>
  );
}

export default MeteoCard;