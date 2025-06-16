import React, { useState, useEffect } from 'react';
import { getPrediction, getFields } from '../services/forecast_service'; // <== додано

function MatchForm() {
  const [matchData, setMatchData] = useState({
    competition_code: '', //
    date: '', //
    home_club_name: '', //
    away_club_name: '', //
    stadium: '', //
    attendance: '', //
    referee: '', //
    home_club_formation: '', //
    away_club_formation: '', //
  });

  const [teams, setTeams] = useState([]); // стан для команд
  const [stadium, setStadium] = useState([]);
  const [referee, setReferee] = useState([]);
  const [competition_codes, setCompetitionCodes] = useState([]);

  const [prediction, setPrediction] = useState(null); // <== додано

  // Завантажити команди при монтуванні компонента
  useEffect(() => {
    const fetchTeams = async () => {
      try {
        const fields = await getFields();
        console.log(fields);
        setTeams(fields.clubs_name || []); // або fields.teams, якщо так називається ключ
        setReferee(fields.referees || []);
        setStadium(fields.stadiums || []);
        setCompetitionCodes(fields.competitions_code || []);

      } catch (error) {
        console.error('Помилка при завантаженні команд:', error);
        setTeams([]);
        setReferee([]);
        setStadium([
          "italy-cup",
          "johan-cruijff-schaal",
          "kypello-elladas",
          "supertaca-candido-de-oliveira"
        ]);
        setCompetitionCodes([]);
      }
    };
    fetchTeams();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setMatchData({ ...matchData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Надсилаємо матч:', matchData);

    try {
      const result = await getPrediction(matchData); // <== запит до API
      console.log(result.predict)
      setPrediction(result.predict); // <== збереження результату
    } catch (error) {
      console.error(error);
      setPrediction({ error: 'Помилка при отриманні прогнозу' });
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Форма матчу</h2>

      <label>
        Вид змагання:
        <select name="competition_code" value={matchData.competition_code} onChange={handleChange} required>
          <option value="">-- Виберіть --</option>
          {competition_codes.map((code) => (
            <option key={code} value={code}>{code}</option>
          ))}
        </select>
      </label>
      <br />

      <label>
        Дата матчу:
        <input type="date" name="date" value={matchData.date} onChange={handleChange} required />
      </label>
      <br />

      <label>
        Домашня команда:
        <select name="home_club_name" value={matchData.home_club_name} onChange={handleChange} required>
          <option value="">-- Виберіть --</option>
          {teams.map((team) => (
            <option key={team} value={team}>{team}</option>
          ))}
        </select>
      </label>
      <br />

      <label>
        Гостьова команда:
        <select name="away_club_name" value={matchData.away_club_name} onChange={handleChange} required>
          <option value="">-- Виберіть --</option>
          {teams.map((team) => (
            <option key={team} value={team}>{team}</option>
          ))}
        </select>
      </label>
      <br />

      <label>
        Місце проведення (Стадіон):
        <select name="stadium" value={matchData.stadium} onChange={handleChange} required>
          <option value="">-- Виберіть --</option>
          {stadium.map((stadium) => (
            <option key={stadium} value={stadium}>{stadium}</option>
          ))}
        </select>
      </label>
      <br />

      <label>
        Відвідуваність:
        <input type="number" name="attendance" value={matchData.attendance} onChange={handleChange} />
      </label>
      <br />

      <label>
        Рефері:
        <select name="referee" value={matchData.referee} onChange={handleChange} required>
          <option value="">-- Виберіть --</option>
          {referee.map((referee) => (
            <option key={referee} value={referee}>{referee}</option>
          ))}
        </select>
      </label>
      <br />

      <label>
        Стартовий склад домашньої команди:
        <input type="text" name="home_club_formation" value={matchData.home_club_formation} onChange={handleChange} />
      </label>
      <br />

      <label>
        Стартовий склад виїзної команди:
        <input type="text" name="away_club_formation" value={matchData.away_club_formation} onChange={handleChange} />
      </label>
      <br />

      <button type="submit">Отримати прогноз</button>

      {/* Відображення прогнозу */}
      {prediction && Array.isArray(prediction) && prediction.length === 2 && (() => {
        const [home, away] = prediction;
        // Простий softmax для ймовірностей
        const expHome = Math.exp(home);
        const expAway = Math.exp(away);
        const expDraw = Math.exp(-Math.abs(home - away));
        const sum = expHome + expAway + expDraw;
        const winProb = (expHome / sum * 100).toFixed(1);
        const drawProb = (expDraw / sum * 100).toFixed(1);
        const loseProb = (expAway / sum * 100).toFixed(1);

        return (
          <div style={{ marginTop: '1rem' }}>
            <strong>Прогнозовані голи:</strong><br />
            Домашня команда: {home.toFixed(2)}<br />
            Гостьова команда: {away.toFixed(2)}<br />
            <br />
            <strong>Ймовірність:</strong><br />
            Перемога домашньої: {winProb}%<br />
            Нічия: {drawProb}%<br />
            Поразка домашньої: {loseProb}%<br />
          </div>
        );
      })()}
      {prediction && prediction.error && (
        <div style={{ marginTop: '1rem', color: 'red' }}>
          <strong>Помилка:</strong> {prediction.error}
        </div>
      )}
    </form>
  );
}

export default MatchForm;
