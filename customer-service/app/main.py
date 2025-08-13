import grpc
from concurrent import futures
import sys
import os
from datetime import datetime, timezone
from database import SessionLocal, Base, Customer
import uuid

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import crm_pb2
import crm_pb2_grpc

class CustomerService(crm_pb2_grpc.CustomerServiceServicer):
    def __init__(self):
        Base.metadata.create_all(bind=SessionLocal().get_bind())


    def get_db(self):
        db = SessionLocal()
        try: return db
        finally: db.close()


    def CreateCustomer(self, request, context):
        db = self.get_db()
        customer_id = f"cust_{uuid.uuid4()}"

        customer = Customer(
            id=customer_id,
            name=request.name,
            email=request.email
        )

        db.add(customer)
        db.commit()
        db.refresh(customer)

        return crm_pb2.CustomerResponse(
            customer=crm_pb2.Customer(
                id=customer.id,
                name=customer.name,
                email=customer.email,
                created_at=customer.created_at.isoformat()
            )
        )
    

    def GetCustomer(self, request, context):
        db = self.get_db()
        customer = db.query(Customer).filter(Customer.id == request.id).first()

        if not customer:
            context.abort(404, "Customer not found")
            return
        
        return crm_pb2.CustomerResponse(
            customer=crm_pb2.Customer(
                id=customer.id,
                name=customer.name,
                email=customer.email,
                created_at=customer.created_at.isoformat()
            )
        )


    def ListCustomers(self, request, context):
        db = self.get_db()
        customers = db.query(Customer).all()
        cust_list = [
            crm_pb2.Customer(
                id=c.id,
                name=c.name,
                email=c.email,
                created_at=c.created_at.isoformat()
            ) for c in customers
        ]
        return crm_pb2.CustomersListResponse(customers=cust_list)


    def UpdateCustomer(self, request, context):
        db = self.get_db()
        customer = db.query(Customer).filter(Customer.id == request.id).first()

        if not customer:
            context.abort(404, "Customer not found")
            return
        
        customer.name = request.name
        customer.email = request.email
        db.commit()

        return crm_pb2.CustomerResponse(
            customer=crm_pb2.Customer(
                id=customer.id,
                name=customer.name,
                email=customer.email,
                created_at=customer.created_at.isoformat()
            )
        )


    def DeleteCustomer(self, request, context):
        db = self.get_db()
        customer = db.query(Customer).filter(Customer.id == request.id).first()

        if not customer:
            context.abort(404, "Customer not found")
            return
        
        db.delete(customer)
        db.commit()
        return crm_pb2.Empty()
    

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    crm_pb2_grpc.add_CustomerServiceServicer_to_server(CustomerService(), server)
    server.add_insecure_port('[::]:50051')
    print("Customer Service запущен. Порт: 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()