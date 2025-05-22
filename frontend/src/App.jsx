import { useState } from 'react'
import logo from './assets/Logo.png'
import './App.css'
import MatchForm from './components/MatchForm'

function App() {


  return (
    <>
      <div className="logo">
        <img src={logo} className="logo" alt="Vite logo" />
        <h1>GamePredictor</h1>
      </div>

      <MatchForm/>
      
    </>
  )
}

export default App
