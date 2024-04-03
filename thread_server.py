import socket
import threading
import time

# Словарь для хранения пользователей и их соответствующих сокетов
users = {}

# Список для хранения истории сообщений
messages = []
logs = []

# Функция для обработки нового эхо пользователя
def echo_client(client_socket):
    while True:
        try:
            # Принимаем данные от клиента
            request = client_socket.recv(1024)
            if not request:
                break
            # Отправляем обратно клиенту данные
            client_socket.send(request)
        except Exception as e:
            print(f"Ошибка при обработке клиента: {e}")
            break
    client_socket.close()

# Функция для обработки подключения нового пользователя
def handle_client(client_socket, username):
    while True:
        try:
            # Получаем сообщение от пользователя
            message = client_socket.recv(1024).decode()
            if message:
                # Добавляем сообщение в историю
                messages.append(f"{username}: {message}")
                logs.append(f"{username}: {message}")
                # Пересылаем сообщение всем остальным пользователям
                for user, user_socket in users.items():
                    if user == username:
                        user_socket.send(f"{username}: {message}".encode())
            else:
                # Если сообщение пустое, закрываем соединение
                client_socket.close()
                del users[username]
                break
        except Exception as e:
            print(f"Ошибка: {e}")
            client_socket.close()
            del users[username]
            break


# Функция для обработки подключения новых пользователей
def accept_connections(server_socket, mode):
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")
        # Получаем имя пользователя
        username = client_socket.recv(1024).decode()
        # Добавляем пользователя в словарь пользователей
        users[username] = client_socket
        # Создаем новый поток для обработки клиента
        if mode == "chat":
            client_handler = threading.Thread(target=handle_client, args=(client_socket, username))
            client_handler.start()
        elif mode == "echo":
            client_handler = threading.Thread(target=echo_client, args=(client_socket,))
            client_handler.start()


# Функция для вывода истории сообщений
def show_messages():
    while True:
        if messages:
            print(messages.pop(0))


# Функция для остановки сервера
def stop_server():
    print("Server stopped")
    time.sleep(1)
    exit()


# Функция для остановки прослушивания портов
def pause_server(server_socket):
    print("Server paused")
    server_socket.close()


# Функция для вывода логов
def show_logs(username):
    for message in logs:
        for user, user_socket in users.items():
            if user == username:
                user_socket.send(f"{message}".encode())
        print(message)


# Функция для очистки логов
def clear_logs():
    logs.clear()


# Функция для очистки файла идентификации
def clear_identification_file():
    # Ваша реализация очистки файла идентификации
    pass


def server(host, port, mode):
    server_socket = open_socket(host, port)

    print(f"Сервер запущен на {host}:{port}")
    # Создаем поток для обработки подключений
    accept_thread = threading.Thread(target=accept_connections, args=(server_socket,mode))
    accept_thread.start()
    # Создаем поток для вывода истории сообщений
    show_messages_thread = threading.Thread(target=show_messages)
    show_messages_thread.start()
    # Создаем управляющий поток
    admin_thread = threading.Thread(target=admin, args=(server_socket, host, port))
    admin_thread.start()


def open_socket(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    return server_socket


def admin(server_socket, host, port):
    while True:
        command = input("Enter command: ")
        if command == "stop":
            stop_server()
        elif command == "pause":
            pause_server(server_socket)
        elif command == "resume":
            open_socket(host, port)
        elif command == "logs":
            show_logs()
        elif command == "clear_logs":
            clear_logs()
        elif command == "clear_identification_file":
            clear_identification_file()


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 1340
    MODE = input("Введите 'echo' или 'chat': ")
    server(HOST, PORT, MODE)
