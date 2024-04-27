import csv
import requests
import clickhouse_connect
import pandas as pd

CLICKHOUSE_CLOUD_HOSTNAME = 'localhost'
CLICKHOUSE_CLOUD_USER = 'default'
CLICKHOUSE_CLOUD_PASSWORD = ''

client = clickhouse_connect.get_client(host=CLICKHOUSE_CLOUD_HOSTNAME, port=8123, username=CLICKHOUSE_CLOUD_USER,
                                       password=CLICKHOUSE_CLOUD_PASSWORD)

data = pd.read_csv('data.csv',  sep = ";", on_bad_lines= "skip", dtype = 'str')

# Define the API endpoints
api_endpoint1 = 'http://api.endpoint1.com'
api_endpoint2 = 'http://localhost:8080/predictions/rubert'

# Send data to API endpoint 1 and endpoint 2, and then send the joined data to ClickHouse server
for index, row in data.iterrows():
    text_data = row[3]
    #response1 = requests.post(api_endpoint1, data=text_data)
    result1 = "хуй"

    response2 = requests.post(api_endpoint2, data=text_data.encode('utf-8'))
    result2 = response2.text

    joined_data = (text_data, result1, result2)
    print(joined_data)

