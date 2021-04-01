import socket


HEADER = 20
PORT = 50050
IP_ADDRESS = socket.gethostbyname(socket.gethostname())
ADDRESS = (IP_ADDRESS, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


if __name__ == "__main__":
    print("To quit type in '!DISCONNECT'")
    doing_stuff = True
    while doing_stuff:
        message = input("Your Message: ")
        send(message)
