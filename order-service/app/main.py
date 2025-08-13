import grpc
from concurrent import futures
import sys
import os
from datetime import datetime, timezone
from database import SessionLocal, Base, Order
import uuid

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import crm_pb2
import crm_pb2_grpc

class OrderService(crm_pb2_grpc.OrderServiceServicer):
    def __init__(self):
        Base.metadata.create_all(bind=SessionLocal().get_bind())

    def get_db(self):
        db = SessionLocal()
        try: return db
        finally: db.close()

    def CreateOrder(self, request, context):
        print(f"Создание заказа: customer_id={request.customer_id}, товар={request.product_name}, цена={request.price}")

        if not request.customer_id:
            context.abort(400, "customer_id is required")
            return
        
        db = self.get_db()
        order_id = f"order_{uuid.uuid4()}"

        order = Order(
            id = order_id,
            customer_id = request.customer_id,
            product_name = request.product_name,
            price = request.price
        )
        db.add(order)
        db.commit()
        db.refresh(order)

        return crm_pb2.OrderResponse(
            order = crm_pb2.Order(
                id = order.id,
                customer_id = order.customer_id,
                product_name = order.product_name,
                price = order.price,
                created_at = order.created_at.isoformat()
            )
        )
    
    def GetCustomerOrders(self, request, context):
        print(f"Получен запрос для customer_id: {request.customer_id}")
        if not request.customer_id:
            context.abort(400, "customer_id is required")
            return

        db = self.get_db()
        try:
            print(f"Поиск заказов для {request.customer_id}")
            order = db.query(Order).filter(Order.customer_id == request.customer_id).all()
            print(f"Найдено заказов: {len(order)}") 
            order_list = [
                crm_pb2.Order(
                    id=o.id,
                    customer_id=o.customer_id,
                    product_name=o.product_name,
                    price=o.price,
                    created_at=o.created_at.isoformat()
                )
                for o in order
            ]
            return crm_pb2.OrderListResponse(orders = order_list)
        except Exception as e:
            print(f"Ошибка в GetCustomerOrders: {e}")
            context.abort(500, "Internal error")
            return
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    crm_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
    server.add_insecure_port('[::]:50052')
    print("Order Service запущен. Порт 50052")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()