import { useState } from 'react'
import logo from './assets/Logo.png'
import './App.css'
import MatchForm from './components/MatchForm'
import { getPrediction } from './services/api'

function App() {
  const [prediction, setPrediction] = useState(null);

  const handleFormSubmit = async (data) => {
    try {
      const result = await getPrediction(data);
      setPrediction(result);
    } catch (error) {
      console.error(error);
      setPrediction("Помилка під час отримання прогнозу.");
    }
  };

  return (
    <>
      <div className="logo">
        <img src={logo} className="logo" alt="Vite logo" />
        <h1>GamePredictor</h1>
      </div>

      <MatchForm onSubmit={handleFormSubmit} />
      {prediction && <div>Прогноз: {JSON.stringify(prediction)}</div>}
      
    </>
  )
}

export default App
