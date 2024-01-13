import socket


def send_request():
    server_host = '127.0.0.1'  # Адрес сервера
    server_port = 8090         # Порт сервера

    # Создаем сокет и подключаемся к серверу
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    # Формируем HTTP-запрос
    request = """GET /?status=200 HTTP/1.1
Host: localhost:8090
User-Agent: MyClient

"""

    # Отправляем запрос серверу
    client_socket.send(request.encode('utf-8'))

    # Получаем ответ от сервера
    response = client_socket.recv(1024)
    print(response.decode('utf-8'))

    # Закрываем соединение
    client_socket.close()


if __name__ == "__main__":
    send_request()
