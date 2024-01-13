import socket
import re
from http import HTTPStatus


def handle_request(client_socket):
    request_data = client_socket.recv(1024).decode('utf-8')
    if not request_data:
        return "если входящий запрос от клиента не содержит данных (пустая строка или None), " \
               "то функция handle_request завершаетcя и соединение с клиентом закрывается"

    # Извлекаем метод из запроса
    method_match = re.search(r'(\w+) /', request_data)                       # r'(\w+) /' - это регулярное выражение
    if method_match:
        request_method = method_match.group(1)
    else:
        request_method = "UNKNOWN"

    # Извлекаем статус из GET параметра
    status_match = re.search(r'GET /.*\?status=(\d{3})', request_data)
    if status_match:
        status_code = int(status_match.group(1))
    else:
        status_code = 200

    # Формируем HTTP-ответ
    response_status = f'{status_code} {HTTPStatus(status_code).phrase}'
    response_headers = {
        'Request Method': request_method,
        'Request Source': client_socket.getpeername(),
        'Response Status': response_status,
    }

    # Отправляем заголовки клиенту
    response = '\n'.join([f'{header}: {value}' for header, value in response_headers.items()])
    client_socket.send(f"{response}\n\n".encode('utf-8'))

    # Закрываем соединение с клиентом
    client_socket.close()

with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as server_socket:
    server_socket.bind(('127.0.0.1', 8090))
    server_socket.listen(1)
    print("Сервер запущен на порту 8090")

    while True:
        client_socket, _ = server_socket.accept()
        handle_request(client_socket)


""" server_socket.listen(1) - сервер будет принимать только одно активное соединение одновременно. Когда клиент 
подключится, сервер примет его соединение и начнет обрабатывать запросы. Если другой клиент попытается подключиться в 
то время, когда сервер уже обслуживает одного клиента, этот клиент будет поставлен в очередь ожидания. 
"""