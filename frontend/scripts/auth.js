function checkAuth() {
    const token = localStorage.getItem('token');
    const isAuthPage = ['login.html', 'register.html'].some(page => window.location.pathname.endsWith(page));

    if (!token && !isAuthPage) {
        window.location.href = 'login.html';
    } else if (token && isAuthPage) {
        window.location.href = 'customers.html';
    }
}


async function login() {
    const status = document.getElementById('status');
    const username = document.getElementById('username');
    status.textContent = 'Вход...';

    try {
        const res = await fetch('http://localhost:8000/login', { method: 'POST' });
        const data = await res.json();
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('username', {username});
        status.textContent = 'Добро пожаловать!';
        setTimeout(() => window.location.href = 'customers.html', 1000);
    } catch (err) {
        status.textContent = `Ошибка подключения к серверу. Ошибка: ${err}`;
    }
}


function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    window.location.href = 'login.html';
}


async function api(url, method = 'GET', body = null) {
    const token = localStorage.getItem('token');
    
    if (!token) {
        console.error('Нет токена в localStorage');
        throw new Error('Не авторизован');
    }

    const options = {
        method,
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    };

    if (body) {
        options.body = JSON.stringify(body);
    }

    const res = await fetch(`http://localhost:8000${url}`, options);

    if (!res.ok) {
        const errorText = await res.text();
        console.error('Ошибка API:', res.status, errorText);
        throw new Error(`Ошибка: ${res.status}`);
    }

    return await res.json();
}

document.addEventListener('DOMContentLoaded', checkAuth);