import socket
import threading
import json


HEADER = 20
PORT = 50551
IP_ADDRESS = socket.gethostbyname(socket.gethostname())
ADDRESS = (IP_ADDRESS, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)


def send(msg):

    msg = json.dumps(msg)
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def receive(client):
    connected = True
    while connected:
        message_specifying_length = client.recv(HEADER).decode(FORMAT)
        if message_specifying_length:
            message_length = int(message_specifying_length)
            message = client.recv(message_length).decode(FORMAT)
            message = json.loads(message)
            print(message)
            if message == "!DISCONNECT":
                connected = False
                client.close()


if __name__ == "__main__":
    print("To quit type in '!DISCONNECT'")
    nickname = input("Nickname: ")
    doing_stuff = True
    threading.Thread(target=receive, args=(client,)).start()
    while doing_stuff:
        content = input("Your Message: ")
        message = {"author": nickname, "content": content, "chat_id": 0}  
        send(message)
