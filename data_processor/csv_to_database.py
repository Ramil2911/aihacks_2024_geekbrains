import csv
import requests
import clickhouse_connect
import pandas as pd
from tqdm import tqdm

CLICKHOUSE_CLOUD_HOSTNAME = 'localhost'
CLICKHOUSE_CLOUD_USER = 'default'
CLICKHOUSE_CLOUD_PASSWORD = ''

client = clickhouse_connect.get_client(host=CLICKHOUSE_CLOUD_HOSTNAME, port=8123, username=CLICKHOUSE_CLOUD_USER,
                                       password=CLICKHOUSE_CLOUD_PASSWORD)

data = pd.read_csv('data.csv',  sep = ";", on_bad_lines= "skip", dtype = 'str')

# Define the API endpoints
api_endpoint1 = 'http://localhost:8080/predictions/classifier'
api_endpoint2 = 'http://localhost:8080/predictions/rubert'

labels = {15: 'технические неполадки', 9: 'конец урока',
 3: 'Начало урока',
 8: 'другое',
 0: 'Возможная отмена урока',
 2: 'На уроке была викторина',
 13: 'предложение ученика',
 17: 'ученик просит помощи',
 6: 'благодарность преподавателю',
 5: 'актив',
 11: 'недовольство программой',
 18: 'юю',
 12: 'непонятная ссылка',
 1: 'Конец урока',
 4: 'Продажа сторонних товаров',
 16: 'учебные ссылки',
 10: 'на уроке была викторина',
 14: 'продажа сторонних товаров',
 7: 'возможная отмена урока'}

# Send data to API endpoint 1 and endpoint 2, and then send the joined data to ClickHouse server
for index, row in data.iterrows():
    text_data = row[3]
    response1 = requests.post(api_endpoint1, data=text_data.encode('utf-8'))
    result1 = response1.text

    response2 = requests.post(api_endpoint2, data=text_data.encode('utf-8'))
    result2 = response2.text

    result1 = labels[int(result1)]
    joined_data = (text_data, result1, result2)
    print(joined_data)

