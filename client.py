import socket
import threading

def receive_messages(client_socket, mode):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message + "\n")
        except Exception as e:
            print(f"Ошибка при получении сообщения: {e}")
            break

def send_messages(client_socket):
    while True:
        try:
            message = input(":")
            client_socket.send(message.encode())
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")
            break

if __name__ == "__main__":
    host = input("Введите IP-адрес сервера: ")
    port = int(input("Введите порт сервера: "))
    username = input("Введите ваше имя: ")
    mode = input("Введите, в каком режиме ваш сервер: ")
    
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        
        # Отправляем имя пользователя на сервер
        client_socket.send(username.encode())
        
        # Создаем потоки для приема и отправки сообщений
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,mode))
        receive_thread.start()
        
        send_thread = threading.Thread(target=send_messages, args=(client_socket,))
        send_thread.start()
        
        receive_thread.join()
        send_thread.join()
    except Exception as e:
        print(f"Ошибка при подключении к серверу: {e}")
    finally:
        client_socket.close()
