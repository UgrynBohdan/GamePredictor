export const getPrediction = async (matchData) => {
  const response = await fetch("http://127.0.0.1:5001/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(matchData)
  });

  if (!response.ok) {
    throw new Error("Помилка при запиті до бекенду");
  }

  return await response.json(); // очікуємо JSON з прогнозом
};

export const getFields = async () => {
  const response = await fetch("http://127.0.0.1:5001/all_fields", {
    method: "GET",
    headers: {
      "Content-Type": "application/json"
    }
  });

  if (!response.ok) {
    throw new Error("Помилка при запиті до бекенду");
  }

  return await response.json(); // очікуємо JSON з прогнозом
};
