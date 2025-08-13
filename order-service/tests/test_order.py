import sys
import os
import pytest
from unittest.mock import MagicMock

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from app.main import OrderService
import crm_pb2


@pytest.fixture
def service():
    """Создаём новый экземпляр сервиса"""
    return OrderService()


@pytest.fixture(autouse=True)
def reset_database(service):
    """Очищаем базу заказов перед каждым тестом"""
    service.orders_db.clear()


def test_create_order(service):
    """Тест: создание заказа"""
    request = crm_pb2.CreateOrdersRequest(
        customer_id="cust_1",
        product_name="Laptop",
        price=999.99
    )
    context = MagicMock()

    response = service.CreateOrder(request, context)

    assert response.order.customer_id == "cust_1"
    assert response.order.product_name == "Laptop"
    assert response.order.price == 999.99
    assert response.order.id is not None
    assert len(service.orders_db) == 1


def test_create_order_missing_customer_id(service):
    """Тест: ошибка при отсутствии customer_id"""
    request = crm_pb2.CreateOrdersRequest(
        product_name="Mouse",
        price=25.50
    )
    context = MagicMock()

    response = service.CreateOrder(request, context)

    context.abort.assert_called_once_with(400, "customer_id is required")


def test_get_customer_orders_empty(service):
    """Тест: заказы отсутствуют"""
    request = crm_pb2.GetCustomerOrdersRequest(customer_id="cust_1")
    context = MagicMock()

    response = service.GetCustomerOrders(request, context)

    assert len(response.orders) == 0


def test_get_customer_orders_with_data(service):
    """Тест: получение заказов клиента"""
    service.CreateOrder(
        crm_pb2.CreateOrdersRequest(customer_id="cust_1", product_name="Book", price=15.0),
        MagicMock()
    )
    service.CreateOrder(
        crm_pb2.CreateOrdersRequest(customer_id="cust_1", product_name="Pen", price=2.5),
        MagicMock()
    )
    service.CreateOrder(
        crm_pb2.CreateOrdersRequest(customer_id="cust_2", product_name="Phone", price=500.0),
        MagicMock()
    )

    request = crm_pb2.GetCustomerOrdersRequest(customer_id="cust_1")
    context = MagicMock()
    response = service.GetCustomerOrders(request, context)

    assert len(response.orders) == 2
    assert response.orders[0].product_name == "Book"
    assert response.orders[1].product_name == "Pen"


def test_get_customer_orders_no_customer_id(service):
    """Тест: ошибка при отсутствии customer_id в запросе"""
    request = crm_pb2.GetCustomerOrdersRequest(customer_id="")
    context = MagicMock()

    response = service.GetCustomerOrders(request, context)

    context.abort.assert_called_once_with(400, "customer_id is required")