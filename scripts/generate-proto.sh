#!/bin/bash

echo "Генерация gRPC кода из proto"

python -m grpc_tools.protoc -Iproto \
    --python_out=api-gateway/app \
    --grpc_python_out=api-gateway/app \
    proto/crm.proto


python -m grpc_tools.protoc -Iproto \
    --python_out=customer-service/app \
    --grpc_python_out=customer-service/app \
    proto/crm.proto


python -m grpc_tools.protoc -Iproto \
    --python_out=order-service/app \
    --grpc_python_out=order-service/app \
    proto/crm.proto

echo "gRPC код сгенерирован в customer-service, order-service, api-gateway"