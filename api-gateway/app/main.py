from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
import grpc
import jwt
import datetime
import sys
from dotenv import load_dotenv
import os
from pydantic import BaseModel

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import crm_pb2
import crm_pb2_grpc

class CustomerCreate(BaseModel):
    name: str
    email: str

class OrderCreate(BaseModel):
    customer_id: str
    product_name: str
    price: float

class CustomerUpdate(BaseModel):
    name: str
    email: str

app = FastAPI(
    title="CRM API",
    version="1.0",
    description="Микросервисная CRM-система",
    contact={
        "name": "Глеб",
        "telegram": "@Visage2",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    debug=True
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
security = HTTPBearer()

load_dotenv()
JWT_ALGORITHM = "HS256"

JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET not installed in the .env file")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_customer_stub():
    channel = grpc.insecure_channel("customer-service:50051")
    return crm_pb2_grpc.CustomerServiceStub(channel)


def get_order_stub():
    channel = grpc.insecure_channel('order-service:50052')
    return crm_pb2_grpc.OrderServiceStub(channel)

@app.post("/register", description="Регистрация пользователей в системе")
def register(username: str = None):
    token = jwt.encode(
        {
            "sub": username or "user",
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
        },
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )
    return {"access_token": token, "token_type": "bearer"}

@app.post("/login", description="Авторизация пользователей в системе")
def login():
    token = jwt.encode(
        {
            "sub": "user",
            "exp": datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc) + datetime.timedelta(hours=24)
        },
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )
    return {"access_token": token, "token_type": "bearer"}


@app.get("/customers", dependencies=[Depends(verify_token)], description="Список клиентов в системе")
def list_customers():
    stub = get_customer_stub()
    try:
        response = stub.ListCustomers(crm_pb2.Empty())
        customers = [
            {
                "id": i.id,
                "name": i.name,
                "email": i.email,
                "created_at": i.created_at
            }
            for i in response.customers
        ]
        return {"customers": customers}
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")


@app.post("/customers", dependencies=[Depends(verify_token)], description="Создание нового клиента в системе")
def create_customer(customer: CustomerCreate):
    stub = get_customer_stub()
    request = crm_pb2.CreateCustomerRequest(name=customer.name, email=customer.email)
    try:
        response = stub.CreateCustomer(request)
        return {
            "id": response.customer.id,
            "name": response.customer.name,
            "email": response.customer.email,
            "created_at": response.customer.created_at
        }
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=e.details())
    

@app.put("/customers/{customer_id}", dependencies=[Depends(verify_token)], description="Обновление данных клиента в системе")
def update_customer(customer_id: str, customer: CustomerUpdate):
    stub = get_customer_stub()
    request = crm_pb2.UpdateCustomerRequest(id=customer_id, name=customer.name, email=customer.email)
    try:
        response = stub.UpdateCustomer(request)
        return {
            "id": response.customer.id,
            "name": response.customer.name,
            "email": response.customer.email,
            "created_at": response.customer.created_at
        }
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=e.details())
    

@app.delete("/customers/{customer_id}", dependencies=[Depends(verify_token)], description="Удаление клиента из системы")
def delete_customer(customer_id: str):
    stub = get_customer_stub()
    request = crm_pb2.DeleteCustomerRequest(id=customer_id)
    try:
        stub.DeleteCustomer(request)
        return {"status": "deleted"}
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=e.details())
    

@app.post("/orders", dependencies=[Depends(verify_token)], description="Создание нового заказа в системе")
def create_order(order: OrderCreate):
    stub = get_customer_stub()
    try:
        customer_request = crm_pb2.GetCustomerRequest(id=order.customer_id)
        customer_response = stub.GetCustomer(customer_request)
        
        if not customer_response.customer:
            raise HTTPException(status_code=404, detail="Клиент не найден")
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(status_code=404, detail="Клиент не найден")
        else:
            raise HTTPException(status_code=500, detail=f"Ошибка сервиса клиентов: {e.details()}")

    stub = get_order_stub()
    request = crm_pb2.CreateOrdersRequest(
        customer_id=order.customer_id,
        product_name=order.product_name,
        price=order.price
    )
    try:
        response = stub.CreateOrder(request)
        return {
            "id": response.order.id,
            "customer_id": response.order.customer_id,
            "product_name": response.order.product_name,
            "price": response.order.price,
            "created_at": response.order.created_at
        }
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=e.details())


@app.get("/orders/customer/{customer_id}", dependencies=[Depends(verify_token)], description="Список заказов в системе")
def get_orders_by_customer(customer_id: str):
    stub = get_order_stub()
    request = crm_pb2.GetCustomerOrdersRequest(customer_id=customer_id)
    try:
        response = stub.GetCustomerOrders(request)
        orders = [
            {
                "id": o.id,
                "product_name": o.product_name,
                "price": o.price,
                "created_at": o.created_at
            }
            for o in response.orders
        ]
        return {"orders": orders}
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()} (code: {e.code().name})")