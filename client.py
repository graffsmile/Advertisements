import uuid

import requests


params_user = {
    'name': 'Mr.Pitkin',
    'password': '12345',
    'role': 'admin',
}

params_adv = {
    'title': 'Летучий Голландец',
    'description': 'Продается корабль, не бит, не крашен, без пробега по Черному морю',
    'price': 100000000
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

# data = requests.get("http://127.0.0.1:8000/api/v1/advertisement?title=Летучий Голландец")
# print(data.status_code)
# print(data.json())

# data = requests.get("http://127.0.0.1:8000/api/v1/user?name=Jack")
# print(data.status_code)
# print(data.json())

data = requests.post("http://127.0.0.1:8000/api/v1/user", json=params_user)
print(data.status_code)
print(data.json())

data = requests.post("http://127.0.0.1:8000/api/v1/login", json=params_user)
print(data.status_code)
print(data.json())
token = data.json()["token"]

data_adv = requests.post("http://127.0.0.1:8000/api/v1/advertisement", json=params_adv, headers={"x-token": token})
print(data_adv.status_code)
print(data_adv.json())

# data = requests.get("http://127.0.0.1:8000/api/v1/advertisement/1")
# print(data.status_code)
# print(data.json())

# data = requests.patch("http://127.0.0.1:8000/api/v1/user/14", json={"password": "125"}, headers={"x-token": token})
# print(data.status_code)
# print(data.json())

# data = requests.patch("http://127.0.0.1:8000/api/v1/advertisement/3", json=patch_params, headers={"x-token": token})
# print(data.status_code)
# print(data.json())

data = requests.delete("http://127.0.0.1:8000/api/v1/advertisement/2", headers={"x-token": token})
print(data.status_code)
print(data.json())

# data = requests.delete("http://127.0.0.1:8000/api/v1/user/11", headers={"x-token": token})
# print(data.status_code)
# print(data.json())
