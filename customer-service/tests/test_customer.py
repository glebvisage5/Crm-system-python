import sys
import os
import pytest
from unittest.mock import MagicMock

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from app.main import CustomerService
import crm_pb2


@pytest.fixture
def service():
    """Создание нового экземпляра сервиса для каждого теста"""
    return CustomerService()


@pytest.fixture(autouse=True)
def reset_database(service):
    """Очищение базы перед каждым тестом"""
    service.customers_db.clear()

def test_create_customer(service):
    """Тест: создание клиента"""
    request = crm_pb2.CreateCustomerRequest(name="Иван Иванов", email="email@email.ru")
    context = MagicMock()

    response = service.CreateCustomer(request, context)

    assert response.customer.name == "Иван Иванов"
    assert response.customer.email == "email@email.ru"
    assert response.customer.id is not None
    assert response.customer.id.startswith("cust_")
    assert len(service.customers_db) == 1


def test_get_customer_existing(service):
    """Тест: получение существующего клиента"""
    create_req = crm_pb2.CreateCustomerRequest(name="Петя", email="email@email.ru")
    create_resp = service.CreateCustomer(create_req, MagicMock())

    get_req = crm_pb2.GetCustomerRequest(id=create_resp.customer.id)
    context = MagicMock()
    response = service.GetCustomer(get_req, context)

    assert response.customer.id == create_resp.customer.id
    assert response.customer.name == "Петя"
    assert response.customer.email == "email@email.ru"


def test_get_customer_not_found(service):
    """Тест: получение несуществующего клиента"""
    get_req = crm_pb2.GetCustomerRequest(id="unknown")
    context = MagicMock()

    response = service.GetCustomer(get_req, context)

    context.abort.assert_called_once_with(404, "Customer not found")


def test_list_customers_empty(service):
    """Тест: список клиентов — пусто"""
    request = crm_pb2.Empty()
    context = MagicMock()
    response = service.ListCustomers(request, context)

    assert len(response.customers) == 0


def test_list_customers_with_data(service):
    """Тест: список клиентов — есть данные"""
    service.CreateCustomer(
        crm_pb2.CreateCustomerRequest(name="Стас", email="stas@email.ru"),
        MagicMock()
    )
    service.CreateCustomer(
        crm_pb2.CreateCustomerRequest(name="Толя", email="tolya@email.ru"),
        MagicMock()
    )

    request = crm_pb2.Empty()
    context = MagicMock()
    response = service.ListCustomers(request, context)

    assert len(response.customers) == 2
    assert response.customers[0].name == "Стас"
    assert response.customers[1].name == "Толя"


def test_create_multiple_customers_ids_unique(service):
    """Тест: ID клиентов уникальны"""
    names = ["Игорь", "Ева", "Степан"]
    ids = []

    for name in names:
        req = crm_pb2.CreateCustomerRequest(name=name, email=f"{name.lower()}@email.ru")
        resp = service.CreateCustomer(req, MagicMock())
        ids.append(resp.customer.id)

    assert len(ids) == len(set(ids)), "ID должны быть уникальными"