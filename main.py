import socket
import threading
from someClasses import *
import json


# server config
HEADER = 20
IP_ADDRESS = socket.gethostbyname(socket.gethostname())
PORT = 50551
ADDRESS = (IP_ADDRESS, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"
FORMAT = "utf-8"


groups = []


def send_messages_to_client(client_handler):
    print("Write the message you want to send")
    while True:
        message = input("Message: ")
        message = json.dumps(message)
        client_handler.notify(message)


def start_server(HEADER=HEADER, IP_ADDRESS=IP_ADDRESS, PORT=PORT, DISCONNECT_MESSAGE=DISCONNECT_MESSAGE, FORMAT=FORMAT):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.close()
    except:
        pass
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDRESS)
    server.listen()
    chats_manager = ChatsManager()
    the_only_group_for_now = Chat("first chat")
    chats_manager.add_chat(the_only_group_for_now)
    working = True

    while working:

        client_socket, client_address = server.accept()
        client_handler = ClientHandler(client_socket, chats_manager)
        threading.Thread(target=send_messages_to_client, args=(client_handler,)).start()
        thread_handling_client = threading.Thread(target=client_handler.receive_messages)
        the_only_group_for_now.add_participant(client_handler)
        print("New Client Added")
        thread_handling_client.start()


if __name__ == "__main__":
    start_server()