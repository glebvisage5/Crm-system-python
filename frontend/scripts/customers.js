let customers = [];


async function loadCustomers() {
    try {
        const data = await api('/customers');
        customers = data.customers;
        renderCustomers();
    } catch (err) {
        document.getElementById('customersList').innerHTML = '<li>Ошибка загрузки</li>';
    }
}


function renderCustomers() {
    const list = document.getElementById('customersList');
    list.innerHTML = customers.map(c => `
        <li>
            (${c.id}) <strong>${c.name}</strong> (${c.email})
            <button onclick="copyId('${c.id}')">Копировать ID</button>
            <button onclick="editCustomer('${c.id}', '${c.name}', '${c.email}')">Редактировать</button>
            <button onclick="deleteCustomer('${c.id}')">Удалить</button>
        </li>
    `).join('');
}


function copyId(id) {
    navigator.clipboard.writeText(id).then(() => {
        alert(`ID скопирован: ${id}`);
    });
}


async function createCustomer() {
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    if (!name || !email) return alert('Заполните все поля');

    try {
        await api('/customers', 'POST', { name, email });
        document.getElementById('name').value = '';
        document.getElementById('email').value = '';
        loadCustomers();
    } catch (err) {
        alert(`Ошибка создания клиента ${err}`);
    }
}


async function editCustomer(id, name, email) {
    const newName = prompt("Имя", name);
    const newEmail = prompt("Email", email);
    if (!newName || !newEmail) return;

    try {
        await api(`/customers/${id}`, 'PUT', { name: newName, email: newEmail });
        loadCustomers();
    } catch (err) {
        alert(`Ошибка обновления ${err}`);
    }
}


async function deleteCustomer(id) {
    if (!confirm('Удалить клиента?')) return;

    try {
        await api(`/customers/${id}`, 'DELETE');
        loadCustomers();
    } catch (err) {
        alert(`Ошибка удаления ${err}`);
    }
}


loadCustomers();