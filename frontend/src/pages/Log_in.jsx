import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { logIn } from '../services/auth_service'

function Log_in({ setUser }) {
    const [form, setForm] = useState({
        email: '',
        password: '',
    });
    const [message, setMessage] = useState('');
    const navigate = useNavigate();

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const res = await logIn({
                email: form.email,
                password: form.password
            });
            setMessage('Вхід успішний!');
            setUser({ username: res.username });
            setTimeout(() => navigate('/'), 100);
        } catch (error) {
            setMessage(error.message || 'Помилка входу');
        }
    };

    return (
        <form onSubmit={handleSubmit} style={{ maxWidth: 350, margin: "0 auto" }}>
            <h2>Вхід</h2>
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
            <button type="submit">Зареєструватися</button>
            {message && <div style={{ marginTop: 10 }}>{message}</div>}
        </form>
    );
}

export default Log_in