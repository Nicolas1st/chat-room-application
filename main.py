import socket
import threading


HEADER = 20
IP_ADDRESS = socket.gethostbyname(socket.gethostname())
PORT = 50050
ADDRESS = (IP_ADDRESS, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"
FORMAT = "utf-8"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)


def handle_client(socket_handling_client, client_address):
    connected = True
    while connected:
        message_specifying_length = socket_handling_client.recv(HEADER).decode(FORMAT)
        if message_specifying_length:
            message_length = int(message_specifying_length)
            message = socket_handling_client.recv(message_length).decode(FORMAT)
            print(message)
            if message == DISCONNECT_MESSAGE:
                connected = False
    socket_handling_client.close()


def start_server():
    working = True
    server.listen()
    while working:
        socket_handling_client, client_address = server.accept()
        thread_handling_client = threading.Thread(target=handle_client, args=(socket_handling_client, client_address))
        print("New Client Added")
        thread_handling_client.start()


if __name__ == "__main__":
    start_server()