# CRM System

## 📑 Задание
Реализовать простую CRM-систему, состоящую из отдельных микросервисов, разделённых по зонам ответственности:
    -API Gateway: REST-интерфейс, авторизация, маршрутизация запросов к микросервисам
    -Customer Service: управление клиентами (CRUD)
    -Order Service: создание заказов
Коммуникация между API Gateway и микросервисами через gRPC.

## Что включено в систему?
Система включает:
- **API Gateway** (FastAPI, JWT, REST)
- **Customer Service** (gRPC + PostgreSQL)
- **Order Service** (gRPC + PostgreSQL)
- **Frontend** (Vanilla JS, HTML/CSS)
- Полная документация через **Swagger (OpenAPI)**
- Поддержка **Docker и Docker Compose**

---

## 🛠️ Стек технологий

| Категория       | Технологии |
|----------------|-----------|
| Backend        | Python, FastAPI, gRPC, SQLAlchemy |
| База данных    | PostgreSQL |
| Frontend       | Vanilla JS, HTML, CSS |
| Инфраструктура | Docker, Docker Compose |
| Тестирование   | pytest |
| Аутентификация | JWT |
| Документация   | Swagger UI, ReDoc |

---

## 🚀 Запуск
### Клонируйте репозиторий
```bash
git clone https://github.com/glebvisage5/Crm-system-python.git
```
### Перейдите в папку
```bash
cd Crm-system-python
```
### Создайте файл .env
```bash
echo "JWT_SECRET=вставьте_свой_токен"
```
### Сгенерируйте gRPC-код
```bash
./scripts/generate-proto.sh
```
### Запустите всю систему
```bash
docker-compose up --build
```
---

## 🌐 Сервисы

| Сервис           | Адрес                      |
|------------------|----------------------------|
| Frontend         | http://localhost:3000      |
| API Gateway      | http://localhost:8000      |
| Swagger (API)    | http://localhost:8000/docs |
| ReDoc            | Docker, Docker Compose     |
| Customer Service | Порт 50051 (gRPC)          |
| Order Service    | Порт 50052 (gRPC)          |

---

## 📚 Документация (Swagger/OpenAPI)
FastAPI автоматически генерирует полноценную OpenAPI-документацию:
- ✅ Swagger UI: http://localhost:8000/docs (Интерактивная документация, можно пробовать запросы)
- ✅ ReDoc: http://localhost:8000/redoc (Удобный вид для чтения)

## 🖼️ Скриншоты интерфейсов
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/4e969a6f-f109-4138-abed-ac57e93ba7b0" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/5a1a3406-cca6-4357-a96e-506a87f7fdf4" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a4eae8f3-337a-460a-b9a8-219c4f90420d" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/6bb8e4fe-a00a-4028-bfe2-bac226d4a150" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/e9ad3315-2e71-40e9-9858-e8d484852cf0" />

## 📝 Примеры запросов
### 1. Получение JWT токена (регистрация)
```bash
curl -X POST http://localhost:8000/register \
  -d "username=admin"
```
### 2. Создание клиента
```bash
curl -X POST http://localhost:8000/customers \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{"name": "Иванов Иван", "email": "email@email.ru"}'
```
### 3. Получение списка клиентов
```bash
curl -X GET http://localhost:8000/customers \
  -H "Authorization: Bearer <ваш-токен>"
```
### 4. Создание заказа
```bash
curl -X POST http://localhost:8000/orders \
  -H "Authorization: Bearer <ваш-токен>" \
  -H "Content-Type: application/json" \
  -d '{"customer_id": "скопированный id", "product_name": "Ноутбук", "price": 500}'
```
### 5. Получение заказов клиентов
```bash
curl -X GET http://localhost:8000/orders/customer/cust_1 \
  -H "Authorization: Bearer <ваш-токен>"
```
## 🧪 Тесты
### Запуск тестов для customer-service
```bash
python -m pytest tests/test_customer.py -v
```
### Запуск тестов для order-service
```bash
python -m pytest tests/test_order.py -v
```

## 🔒 Безопасность
- 🔐 JWT — аутентификация через Authorization: Bearer<token>
- 🌐 CORS — разрешён только http://localhost:3000
- 🔒 .env — JWT_SECRET не попадает в репозиторий
- 🐳 Docker — полная изоляция сервисов

## 🧱 Архитектура
Frontend (Vanilla JS) -> API Gateway (FastAPI, JWT, REST) -> customer-service (gRPC + PostgreSQL) -> order-service    (gRPC + PostgreSQL)

## 📂 Структура проекта
```bash
crm-system-kaspersky
|-> api-gateway - FastAPI + JWT + gRPC клиенты
|-> customer-service - gRPC + PostgreSQL
|-> frontend - HTML, CSS, JS
|-> order-service - gRPC + PostgreSQL
|-> proto - файлы для gRPC-кодов
|-> scripts
||-> generate-proto.sh - генерация gRPC-кодов
|-> .gitignore - файлы для игнорирования git
|-> .env - ключи, токены и т.п.
|-> docker-compose.yml - контейнеры для запуска сервисов
|-> README.md
```

## 🎯 Сделано согласно ТЗ
- API Gateway (FastAPI, REST + JWT + gRPC clients)
- - POST /register — регистрация пользователя
- - POST /login — вход, возвращает JWT
- - CRUD /customers — маршрутизирует к Customer Service через gRPC
- - POST /orders — маршрутизирует заказ в Order Service через gRPC
- - Middleware для проверки JWT

- Customer Service (gRPC Server)
- - CreateCustomer
- - GetCustomer
- - UpdateCustomer
- - DeleteCustomer
- - ListCustomers

- Order Service (gRPC Server)
- - CreateOrder
- - GetCustomerOrder
- - Каждый заказ связан с customer_id

- Frontend:
- - Форма регистрации/логина (сохранение JWT в localStorage)
- - Просмотр списка клиентов
- - Создание клиента
- - Обновление клиента
- - Удаление клиента
- - Создание заказа
- - Просмотр заказов по клиенту

- Тесты: pytest
- База Данных: PostgreSql
- Документация (Swagger/OpenAPI)

## 📬 Контакты
Telegram: @Visage2
