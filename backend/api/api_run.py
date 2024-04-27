from fastapi import FastAPI
import clickhouse_connect
from fastapi.middleware.cors import CORSMiddleware

CLICKHOUSE_CLOUD_HOSTNAME = 'localhost'
CLICKHOUSE_CLOUD_USER = 'default'
CLICKHOUSE_CLOUD_PASSWORD = ''

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = clickhouse_connect.get_client(host=CLICKHOUSE_CLOUD_HOSTNAME, port=8123, username=CLICKHOUSE_CLOUD_USER,
                                       password=CLICKHOUSE_CLOUD_PASSWORD)

client.command('CREATE DATABASE IF NOT EXISTS chatbot')
client.command(
    'CREATE TABLE IF NOT EXISTS chatbot.chat_history (conversation_id int, sender String, message String) ENGINE = MergeTree ORDER BY conversation_id')
client.command(
    'CREATE TABLE IF NOT EXISTS chatbot.records (id int, sender String, message String, timestamp String, score int, positivity float, class String) ENGINE = MergeTree ORDER BY score')


@app.post("/chatbot/{conversation_id}/{sender}")
async def chatbot(conversation_id: int, message: str):
    response = get_ai_response(message)
    if response:
        client.insert('chatbot.chat_history', [(conversation_id, 'user', message), (conversation_id, 'bot', response)])
        return response
    else:
        return "Sorry, I'm having trouble generating a response right now. Please try again later."


def get_ai_response(message):
    # Placeholder AI response generation logic
    # In this example, the AI response is generated randomly
    import random
    if random.random() < 0.5:  # 50% chance of failing
        return None
    else:
        return "Placeholder AI response for message: " + message


@app.get("/chat_history/{conversation_id}")
async def get_chat_history(conversation_id: str):
    result = client.query('SELECT sender, message FROM chatbot.chat_history WHERE conversation_id = {id:Int64}',
                          parameters={"id": conversation_id})
    chat_history = [{"sender": row[0], "message": row[1]} for row in result.result_rows]
    return chat_history


@app.get("/chats")
async def get_chats():
    result = client.query("SELECT DISTINCT conversation_id from chatbot.chat_history")
    return result.result_rows


@app.post("https://backend.example.com/chats/{chatId}/messages")
async def get_chat_messages(chatId: int):
    pass


@app.get("/chats/{chatId}/metrics")
async def get_metrics(chatId: int):
    pass


@app.get("/chats/{chatId}/messages")
async def get_messages(chatId: int):
    pass
