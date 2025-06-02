export const singIn = async (matchData) => {
  const response = await fetch("http://127.0.0.1:5002/register", {
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

export const logIn = async (matchData) => {
  const response = await fetch("http://127.0.0.1:5002/login", {
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
