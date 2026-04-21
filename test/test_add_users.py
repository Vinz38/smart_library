from requests import post, get, delete, put
import json


headers = {
    "SECRET_KEY": "123sold123"
}

'''response1 = post('http://127.0.0.1:5050/api/users', json={
    "surname": "Никулин",
    "name": "Илья",
    "middlename": "Алексеевич",
    "email": "ilia.nikulin09@gmail.com",
    "class_name": "10фми-1"
}, headers=headers)

response2 = post('http://127.0.0.1:5050/api/users', json={
    "surname": "Епишкин",
    "name": "Кирилл",
    "middlename": "Максимович",
    "email": "kirillepiskin.gmail.com",
    "class_name": "10фми-1"
}, headers=headers)

response3 = post('http://127.0.0.1:5050/api/users', json={
    "surname": "Базин",
    "name": "Женя",
    "middlename": "Павлович",
    "email": "jenek",
    "class_name": "10фми-1"
}, headers=headers)

response4 = post('http://127.0.0.1:5050/api/users', json={
    "surname": "Бобков",
    "name": "Никита",
    "middlename": "Лохович",
    "email": "nikitos",
    "class_name": "10фми-1"
}, headers=headers)'''

'''response5 = put('http://127.0.0.1:5050/api/users/2', json={
    "surname": "Никулин",
    "name": "Илья",
    "middlename": "Алексеевич",
    "email": "ilia.nikulin09@gmail.com",
    "class_name": "10фми-1",
    "book_list": {"Повелитель мух": ["Уильям Голдинг", "978-5-17-080086-5"]},
    "textbook_list": {"Алгебра углубленный уровень": ["Алгебра", "10 класс", "Мерзляк"]}}, headers=headers)'''

'''
response6 = delete('http://127.0.0.1:5050/api/users/2', headers=headers)
response6 = delete('http://127.0.0.1:5050/api/add_users/7', headers=headers)
response6 = delete('http://127.0.0.1:5050/api/add_users/8', headers=headers)
response6 = delete('http://127.0.0.1:5050/api/add_users/9', headers=headers)
response6 = delete('http://127.0.0.1:5050/api/add_users/10', headers=headers)
response6 = delete('http://127.0.0.1:5050/api/add_users/11', headers=headers)
response6 = delete('http://127.0.0.1:5050/api/add_users/12', headers=headers)
'''

response7 = get('http://127.0.0.1:5050/api/users', headers=headers)
data = response7.json()
print(data)

'''
print(json.dumps(data, indent=4, ensure_ascii=False))
print(response5.status_code)
print(response5.text)'''
