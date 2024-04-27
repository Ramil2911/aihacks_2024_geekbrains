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

client = clickhouse_connect.get_client(host=CLICKHOUSE_CLOUD_HOSTNAME, port=8123, username=CLICKHOUSE_CLOUD_USER, password=CLICKHOUSE_CLOUD_PASSWORD)

client.execute('CREATE DATABASE IF NOT EXISTS chatbot')
client.execute('CREATE TABLE IF NOT EXISTS chatbot.chat_history (conversation_id String, sender String, message String) ENGINE = MergeTree ORDER BY conversation_id')

@app.post("/chatbot/{conversation_id}/{sender}")
async def chatbot(conversation_id: str, sender: str, message: str):
    response = get_ai_response(message)
    if response:
        client.execute('INSERT INTO chatbot.chat_history (conversation_id, sender, message) VALUES', [(conversation_id, sender, message)])
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
    result = client.execute('SELECT sender, message FROM chatbot.chat_history WHERE conversation_id = %s', (conversation_id,))
    chat_history = [{"sender": row[0], "message": row[1]} for row in result]
    return chat_history