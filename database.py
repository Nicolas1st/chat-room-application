import sqlite3


DATABASE_NAME = "chatapp.db"


connection = sqlite3.connect(DATABASE_NAME)
cursor = connection.cursor()


def initialize_tables(cursor=cursor, database_name=DATABASE_NAME):

    try:

        cursor.execute("""
        CREATE TABLE users (
            id INTEGER NOT NULL PRIMARY KEY,
            nickname varchar(20) NOT NULL,
            password varchar(100) NOT NULL
        );
        """)


        cursor.execute("""
        CREATE TABLE messages (
            id INTEGER NOT NULL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            chat_id INTEGER NOT NULL,
            message text NOT NULL
        );
        """)


        cursor.execute("""
        CREATE TABLE chats (
            id INTEGER NOT NULL PRIMARY KEY,
            name varchar(50) NOT NULL
        );
        """)


        cursor.execute("""
        CREATE TABLE memberships (
            id INTEGER NOT NULL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            chat_id INTEGER NOT NULL
        );
        """)

    except: 
        pass


def store_new_user(nickname, password, cursor=cursor):
    cursor.execute("""INSERT INTO users (nickname, password) VALUES (?, ?)""", (nickname, password))


def store_new_message(chat_id, user_id, message, cursor=cursor):
    cursor.execute("""INSERT INTO messages (chat_id, user_id, message) VALUES (?, ?, ?)""", (chat_id, user_id, message))


def store_new_chat(user_id, chat_id, cursor=cursor):
    cursor.execute("""INSERT INTO chats (user_id, chat_id) VALUES (?, ?)""", (user_id, chat_id))


if __name__ == "__main__":
    initialize_tables()
