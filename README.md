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

## 🌐 Сервисы
