let orders = [];
let currentCustomerId = null;
const date = new Date(order.created_at).toLocaleString('ru-RU');

async function createOrder() {
    const customerId = document.getElementById('customerId').value;
    const productName = document.getElementById('productName').value;
    const price = parseFloat(document.getElementById('price').value);

    if (!customerId || !productName || isNaN(price)) {
        return alert('Заполните все поля');
    }

    try {
        await api('/orders', 'POST', { 
            customer_id: customerId, 
            product_name: productName, 
            price 
        });
        alert('Заказ создан');
        
        if (currentCustomerId === customerId) {
            getOrders();
        }
    } catch (err) {
        if (err.message.includes('404') && err.message.includes('Клиент не найден')) {
            alert(`Ошибка: клиент с ID "${customerId}" не существует`);
        } else {
            alert(`Ошибка: ${err.message}`);
        }
    }
}


async function getOrders() {
    const input = document.getElementById('ordersCustomerId');
    const customerId = input.value.trim();

    if (!customerId) {
        return alert('Введите ID клиента');
    }

    try {
        const data = await api(`/orders/customer/${customerId}`);
        orders = data.orders || [];
        currentCustomerId = customerId;

        renderOrders();
    } catch (err) {
        console.error('Ошибка при загрузке заказов:', err);
        document.getElementById('ordersList').innerHTML = '<li>Ошибка загрузки заказов</li>';
    }
}


function renderOrders() {
    const list = document.getElementById('ordersList');

    if (orders.length === 0) {
        list.innerHTML = '<li>Нет заказов</li>';
        return;
    }

    list.innerHTML = orders.map(order => `
        <li>
            <strong>${order.product_name}</strong> — ${order.price.toFixed(2)} руб.
            <small> (${new Date(order.created_at).toLocaleString('ru-RU')})</small>
        </li>
    `).join('');
}