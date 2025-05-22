import React, { useState } from 'react';

const teams = ['Real Madrid', 'Barcelona', 'Manchester City', 'Bayern Munich'];

function MatchForm() {
  const [matchData, setMatchData] = useState({
    date: '',
    homeTeam: '',
    awayTeam: '',
    location: '',
    // score: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setMatchData({ ...matchData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Матч збережено:', matchData);
    // Тут можеш відправити matchData на сервер або зберегти в state
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Форма матчу</h2>

      <label>
        Дата матчу:
        <input type="date" name="date" value={matchData.date} onChange={handleChange} required />
      </label>
      <br />

      <label>
        Домашня команда:
        <select name="homeTeam" value={matchData.homeTeam} onChange={handleChange} required>
          <option value="">-- Виберіть --</option>
          {teams.map((team) => (
            <option key={team} value={team}>{team}</option>
          ))}
        </select>
      </label>
      <br />

      <label>
        Гостьова команда:
        <select name="awayTeam" value={matchData.awayTeam} onChange={handleChange} required>
          <option value="">-- Виберіть --</option>
          {teams.map((team) => (
            <option key={team} value={team}>{team}</option>
          ))}
        </select>
      </label>
      <br />

      <label>
        Місце проведення:
        <input type="text" name="location" value={matchData.location} onChange={handleChange} />
      </label>
      <br />

      {/* <label>
        Рахунок:
        <input type="text" name="score" value={matchData.score} onChange={handleChange} placeholder="2-1" />
      </label> */}
      {/* <br /> */}

      <button type="submit">Зберегти матч</button>
    </form>
  );
}

export default MatchForm;
