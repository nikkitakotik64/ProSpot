import requests

ip = 'https://prospot.pythonanywhere.com/search'
params = {'api_key': '1234', 'game': 'cs2'}
response = requests.get(ip, json=params).json()
print(response['status'])
print(response['message'])
print()

params['api_key'] = ''  # подставить сюда свой api-ключ
response = requests.get(ip, json=params).json()
print(response['status'])
print(response['data']['descriptions'])
print(*response['data']['maps'])
print()

params['map'] = 'Dust II'
response = requests.get(ip, json=params).json()
print(response['status'])
print(*response['data']['descriptions'])
