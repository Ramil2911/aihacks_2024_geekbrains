from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI()
root = 

# Наша модель инференс
model = joblib.load("model/my_model.pkl")
model_classes = 
# Модель данных для пользователя
class User(BaseModel):
    id: int = 1

class Message(BaseModel):
    message: str
# --------------------------------------------------------
# 
# --------------------------------------------------------

def CsvReader(root):
    return pd.read_csv(root)

# users_db - будущая бд

def check_string_in_csv(search_string):
    file_path = "chat_data.csv"
    data = pd.read_csv(file_path, header=None, squeeze=True)
    if search_string in data.values:
        return True
    else:
        return False

# --------------------------------------------------------
# Sending message (3)
# --------------------------------------------------------
@app.post("/chats/{chat_id}")
def send_message(chat_id: int, message: Message):
    direct = f'./{chat_id}/{chat_id}.csv'
    if (check_string_in_csv(str(chat_id))):
        raise HTTPException(status_code=404, detail="Chat not found")
    # запрос
    chat = CsvReader(direct)
    new_row = pd.Series([message.message], index=chat.columns)
    chat = chat.append(new_row, ignore_index=True)
    # ответ модели
    answer = model.predict(message)
    new_row = pd.Series([answer], index=chat.columns)
    # сохраняем файл
    chat.to_csv(direct, index=False)

    return {"message": "Message sent successfully"}

# --------------------------------------------------------
# Getting chat data (4)
# --------------------------------------------------------
@app.get("/chats/{chat_id}")
def get_chat_from_id(chat_id: int):
    if (~check_string_in_csv(str(chat_id))):
        raise HTTPException(status_code=404, detail="Chat not found")
    direct = f'./{chat_id}/{chat_id}.csv'
    chat = CsvReader(direct)
    json_data = chat.to_json(orient='records')
    return json_data

@app.get(".") # <-------------------------------- точку можно?
def get_all_chat_id():
    direct = f'chat_data.csv'
    chat_data = CsvReader(direct)
    json_data = chat_data.to_json(orient='records')
    return json_data

# 4.1
@app.get("/chats/{chat_id}")
def get_chat(chat_id: int):
    return

# --------------------------------------------------------
# Getting metrics (2)
# --------------------------------------------------------
def get_model_metric(path): # <--------------------------------------------------- как хранится модель,
                                                # если мы не её будем показывать как конечный результат
    return 

@app.post("./dataset") # <---------------------------------------------------------
def load_data():
    return

@app.get("/dataset") # <-------------------------------------------------- загрузка файлов пользователем?
def get_metric(selected_video: str): #<----------------------------- type?
    direct = f"./dataset/{str}"
    json_data = pd.read_json(direct)
    return json_data

# --------------------------------------------------------
# Add new chat (5)
# --------------------------------------------------------


















# trash

    # # добавление в базу индексов
    # chat_data = CsvReader(f"{chat_id}.csv")
    # new_row = pd.Series([chat_id], index=chat_data.columns)
    # chat_data = chat_data.append(new_row, ignore_index=True)

    # #
    # chat_data = CsvReader(f"./{chat_id}/{chat_id}.csv")

    # return {"message": "Message sent successfully"}