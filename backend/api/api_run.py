from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import clickhouse_connect
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

CLICKHOUSE_CLOUD_HOSTNAME = 'clickhouse'
CLICKHOUSE_CLOUD_USER = 'default'
CLICKHOUSE_CLOUD_PASSWORD = ''

client = clickhouse_connect.get_client(host=CLICKHOUSE_CLOUD_HOSTNAME, port=8123, username=CLICKHOUSE_CLOUD_USER,
                                       password=CLICKHOUSE_CLOUD_PASSWORD)

client.command('CREATE DATABASE IF NOT EXISTS chatbot')
client.command(
    'CREATE TABLE IF NOT EXISTS chatbot.chats (id String, name String, is_favorite UInt8) ENGINE = MergeTree ORDER BY id')
client.command(
    'CREATE TABLE IF NOT EXISTS chatbot.messages (id UUID, chat_id String, sender String, message String, timestamp DateTime) ENGINE = MergeTree ORDER BY (chat_id, timestamp)')

class Chat(BaseModel):
    id: str
    name: str
    is_favorite: bool

class Message(BaseModel):
    id: str
    chat_id: str
    sender: str
    message: str
    timestamp: datetime

def get_chats_from_db():
    query = "SELECT id, name, is_favorite FROM chatbot.chats"
    result = client.query(query)
    return result

def create_chat_in_db(chat: Chat):
    query = "INSERT INTO chatbot.chats (id, name, is_favorite) VALUES (%s, %s, %s)"
    client.query(query, (chat.id, chat.name, chat.is_favorite))

def get_messages_from_db(chat_id: str):
    query = f"SELECT id, chat_id, sender, message, timestamp FROM chatbot.messages WHERE chat_id = '{chat_id}'"
    result = client.query(query)
    return result

def send_message_to_db(chat_id: str, message: Message):
    query = "INSERT INTO chatbot.messages (id, chat_id, sender, message, timestamp) VALUES (%s, %s, %s, %s, %s)"
    client.query(query, (message.id, chat_id, message.sender, message.message, message.timestamp))

# Заглушки данных
def get_stub_chats():
    return [
        {"id": "1", "name": "Chat 1", "is_favorite": False},
        {"id": "2", "name": "Chat 2", "is_favorite": True},
    ]

def get_stub_messages(chat_id: str):
    return [
        {"id": str(uuid.uuid4()), "chat_id": chat_id, "sender": "User 1", "message": "Hello", "timestamp": datetime.now()},
        {"id": str(uuid.uuid4()), "chat_id": chat_id, "sender": "User 2", "message": "Hi there", "timestamp": datetime.now()},
    ]

@app.get("/chats")
async def get_chats():
    try:
        return get_chats_from_db()
    except Exception as e:
        print(f"Error fetching chats from database: {e}")
        return get_stub_chats()

@app.post("/chats")
async def create_chat(chat: Chat):
    try:
        create_chat_in_db(chat)
        return {"success": True, "chat_id": chat.id}
    except Exception as e:
        print(f"Error creating chat in database: {e}")
        return {"success": False}

@app.post("/chats/{chat_id}/messages")
async def send_message(chat_id: str, message: Message):
    try:
        send_message_to_db(chat_id, message)
        return {"success": True}
    except Exception as e:
        print(f"Error sending message to database: {e}")
        return {"success": False}

@app.get("/chats/{chat_id}/messages")
async def get_messages(chat_id: str):
    try:
        return get_messages_from_db(chat_id)
    except Exception as e:
        print(f"Error fetching messages from database: {e}")
        return get_stub_messages(chat_id)
