from binance.client import Client
from json import load

file = open('config/testnet_api.json', 'r')

data = load(file)

api_key = data['api_key']
api_secret = data['api_secret']

client = Client(api_key, api_secret)
client.API_URL = 'https://testnet.binance.vision/api'

client_export = client
