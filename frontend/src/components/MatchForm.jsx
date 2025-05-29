import React, { useState, useEffect } from 'react';
import { getPrediction, getFields } from '../services/api'; // <== додано

// "competition_code": "trophee-des-champions",
// "date": "2025-05-29",
// "home_club_name": "Stade de Reims",
// "away_club_name": "FC Metz",
// "stadium": "Stade Auguste-Delaune",
// "attendance": 21684,
// "referee": "Eric Wattellier",
// "home_club_formation": "4-2-3-1",
// "away_club_formation": "4-2-3-1"
function MatchForm() {
  const [matchData, setMatchData] = useState({
    competition_code: '', //
    date: '', //
    home_club_name: '', //
    away_club_name: '', //
    stadiums: '', //
    attendance: '', //
    referees: '', //
    home_club_formation: '', //
    away_club_formation: '', //
  });

  const [teams, setTeams] = useState([]); // стан для команд
  const [stadiums, setStadiums] = useState([]);
  const [referees, setReferees] = useState([]);

  const [prediction, setPrediction] = useState(null); // <== додано

  // Завантажити команди при монтуванні компонента
  useEffect(() => {
    const fetchTeams = async () => {
      try {
        const fields = await getFields();
        setTeams(fields.clubs_name || []); // або fields.teams, якщо так називається ключ
        setReferees(fields.referee || []);
        setStadiums(fields.stadiums || []);

      } catch (error) {
        console.error('Помилка при завантаженні команд:', error);
        setTeams([]);
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
      setPrediction(result); // <== збереження результату
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
        <input type="text" name="competition_code" value={matchData.competition_code} onChange={handleChange} />
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
        <select name="stadiums" value={matchData.stadiums} onChange={handleChange} required>
          <option value="">-- Виберіть --</option>
          {stadiums.map((stadiums) => (
            <option key={stadiums} value={stadiums}>{stadiums}</option>
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
        <select name="referees" value={matchData.referees} onChange={handleChange} required>
          <option value="">-- Виберіть --</option>
          {referees.map((referees) => (
            <option key={referees} value={referees}>{referees}</option>
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
      {prediction && (
        <div style={{ marginTop: '1rem' }}>
          <strong>Прогноз:</strong> {prediction.error || JSON.stringify(prediction)}
        </div>
      )}
    </form>
  );
}

export default MatchForm;
