import requests


params_user = {
    'name': 'Miki Pirson',
    'password': '12345',
}

params_adv = {
    'title': 'Vaz2101',
    'description': 'Продается корабль, не бит, не крашен, без пробега по Черному морю',
    'price': 100000000,
    'author_id': 2,
}

patch_params = {
    'description': 'Продается машина без пробега по уралу',
    'price': 150000,
}

# data_adv = requests.post("http://127.0.0.1:8000/api/v1/advertisement", json=params_adv)
# print(data_adv.status_code)
# print(data_adv.json())

# data = requests.patch("http://127.0.0.1:8000/api/v1/advertisement/2", json=patch_params)
# print(data.status_code)
# print(data.json())

# data = requests.delete("http://127.0.0.1:8000/api/v1/advertisement/2")
# print(data.status_code)
# print(data.json())

# data = requests.get("http://127.0.0.1:8000/api/v1/advertisement/1")
# print(data.status_code)
# print(data.json())

data = requests.get("http://127.0.0.1:8000/api/v1/advertisement?title=Летучий Голландец")
print(data.status_code)
print(data.json())

# data = requests.post("http://127.0.0.1:8000/api/v1/user", json=params_user)
# print(data.status_code)
# print(data.json())

# data = requests.get("http://127.0.0.1:8000/api/v1/user/1")
# print(data.status_code)
# print(data.json())

# data = requests.patch("http://127.0.0.1:8000/api/v1/user/5", json={"password": "321"})
# print(data.status_code)
# print(data.json())

# data = requests.delete("http://127.0.0.1:8000/api/v1/user/5")
# print(data.status_code)
# print(data.json())