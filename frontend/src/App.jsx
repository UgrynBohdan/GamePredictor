import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import logo from './assets/Logo.png'
import './App.css'
import './pages/Sing_up'
import './pages/Log_in'
import MatchForm from './components/MatchForm'
import { getPrediction } from './services/forecast_service'
import Sing_up from './pages/Sing_up'
import Log_in from './pages/Log_in';

function App() {
  const [prediction, setPrediction] = useState(null);
  const [user, setUser] = useState(null);

  return (
    <Router>
      {user && (
        <div className="user-info">
          <button className="user-btn" onClick={() => setUser(null)}>
            <img src={logo} alt="Logo" className="user-logo" />
            {user.username}
          </button>
        </div>
      )}

      {!user && (
      <div className='buttons_sing_log'>
        <Link to="/register">
          <button>Реєстрація</button>
        </Link>
        <Link to="/login">
          <button>Вхід</button>
        </Link>
      </div>
      )}

      <div className="logo">
        <img src={logo} alt="Logo" className="logo-icon" />
        <span className="logo-text">GamePredictor</span>
      </div>


      <Routes>
        {/* <Route path="/" element={<MatchForm onSubmit={handleFormSubmit} />} /> */}
        <Route path="/" element={<MatchForm />} />
        <Route path="/register" element={<Sing_up setUser={setUser} />} />
        <Route path='/login' element={<Log_in setUser={setUser} />} />
      </Routes>

    </Router>
  )
}

export default App
