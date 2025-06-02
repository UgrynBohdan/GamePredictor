import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { singIn } from '../services/auth_service'

function Sing_up({ setUser }) {
    const [form, setForm] = useState({
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
    });
    const [message, setMessage] = useState('');
    const navigate = useNavigate();

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (form.password !== form.confirmPassword) {
            setMessage('Паролі не співпадають!');
            return;
        }

        try {
            const res = await singIn({
                username: form.username,
                email: form.email,
                password: form.password
            });
            setMessage('Реєстрація успішна!');
            setUser({ username: res.username });
            setTimeout(() => navigate('/'), 100);
        } catch (error) {
            setMessage(error.message || 'Помилка реєстрації');
        }

        setMessage('Реєстрація успішна!');
    };

    return (
        <form onSubmit={handleSubmit} style={{ maxWidth: 350, margin: "0 auto" }}>
            <h2>Реєстрація</h2>
            <label>
                Логін:
                <input
                    type="text"
                    name="username"
                    value={form.username}
                    onChange={handleChange}
                    required
                />
            </label>
            <br />
            <label>
                Email:
                <input
                    type="email"
                    name="email"
                    value={form.email}
                    onChange={handleChange}
                    required
                />
            </label>
            <br />
            <label>
                Пароль:
                <input
                    type="password"
                    name="password"
                    value={form.password}
                    onChange={handleChange}
                    required
                />
            </label>
            <br />
            <label>
                Підтвердіть пароль:
                <input
                    type="password"
                    name="confirmPassword"
                    value={form.confirmPassword}
                    onChange={handleChange}
                    required
                />
            </label>
            <br />
            <button type="submit">Зареєструватися</button>
            {message && <div style={{ marginTop: 10 }}>{message}</div>}
        </form>
    );
}

export default Sing_up