import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import React from 'react';
import Home from "../Pages/Home";
import MeteoCard from '../Components/MeteoCard';

function AppRouter() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/meteo" element={<MeteoCard />} />
      </Routes>
    </Router>
  );
}

export default AppRouter;