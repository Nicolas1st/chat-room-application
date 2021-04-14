from datetime import datetime
import json
import socket


class ChatsManager:

    
    next_group_id = 0


    def __init__(self):
        
        self.chats = {} 


    def add_chat(self, chat):
        
        self.chats[ChatsManager.next_group_id] = chat
        ChatsManager.next_group_id += 1


    def remove_chat(self, chat):
        
        self.chats.pop(chat, None)


    def route_message(self, message):

        """
        Routes to the corresponding receipients

        Input:
            Dictionary containg:
                - author,
                - chat_id,
                - content

        Output:
            None
        """

        chat_id = message["chat_id"]
        chat = self.chats.get(chat_id, None)

        if chat:

            chat.notify_participants(message)
        
        else:

            # do nothing for now
            # figure it out later

            pass


class Chat:


    def __init__(self, name):

        self.name = name
        self.participants = [] 
        self.messages = [] 


    def add_participant(self, participant):

        if participant not in self.participants:
            self.participants.append(participant)


    def remove_participant(self, participant):

        try:
            self.participants.remove(participant)
        except:
            pass


    def notify_participants(self, message):

        for participant in self.participants:
            participant.notify(message)
            self.messages.append(message)


    def add_message(self, message):

        self.messages.append(message)
        message = json.dumps(mesgage.__dict__)
        self.notify_participants(message)


# class Message:
#     
#     time_units = ["year", "month", "day", "hour", "minutes"]
# 
#     def __init__(self, author_name, message):
#         self.author_name = author_name
#         self.message = message
#         time_values = datetime.utcnow().strftime('%B %Y %d %H %M').split(' ')
#         self.time = {time_unit: time_value for time_unit, unit_value in zip(time_units, time_values)}
    

class ClientHandler:


    FORMAT = "utf-8"
    HEADER = 20
    DISCONNECT_MESSAGE = "!DISCONNECT"


    def __init__(self, client_socket, chats_manager):

        self.nickname = None
        self.client_socket = client_socket
        self.chats_manager = chats_manager


    def notify(self, message):
        
        if message["author"] == self.nickname:
            return
        message = json.dumps(message)
        message = message.encode(ClientHandler.FORMAT)
        message_length = len(message)
        send_length = str(message_length).encode(ClientHandler.FORMAT)
        send_length += b' ' * (ClientHandler.HEADER - len(send_length))
        self.client_socket.send(send_length)
        self.client_socket.send(message)


    @staticmethod
    def save_time():

        time_units = ["year", "month", "day", "hour", "minutes"]
        time_values = datetime.utcnow().strftime('%B %Y %d %H %M').split(' ')
        time = {time_unit: time_value for time_unit, time_value in zip(time_units, time_values)}
        return time

    
    def receive_messages(self):

        connected = True
        while connected:
            message_specifying_length = self.client_socket.recv(ClientHandler.HEADER)
            if message_specifying_length:
                message_length = int(message_specifying_length)
                message = self.client_socket.recv(message_length).decode(ClientHandler.FORMAT)
                message = json.loads(message)
                if self.nickname == None:
                    self.nickname = message["author"]
                if message["content"] == ClientHandler.DISCONNECT_MESSAGE:
                    connected = False
                    continue
                message["time"] = ClientHandler.save_time() 
                self.chats_manager.route_message(message)
                print(message)

        self.client_socket.close()
