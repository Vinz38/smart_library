from requests import post, get, delete, put
import json

headers = {
    "SECRET_KEY": "123sold123"
}

response1 = post('http://127.0.0.1:5050/api/book', json={
    "namebook": "Повелитель мух",
    "name_author": "Уильям Голдинг",
    "isbn": "978-5-17-080086-5",
    "yep": 2023,
    "taken": False, 
    "tbw": "-"
}, headers=headers)


response2 = post('http://127.0.0.1:5050/api/book', json={
    "namebook": "Война и Мир",
    "name_author": "Толстой",
    "isbn": "123123",
    "yep": 1959,
    "taken": False,
    "tbw": "-"
}, headers=headers)

response3 = post('http://127.0.0.1:5050/api/book', json={
    "namebook": "Билл герой галактики",
    "name_author": "Гарри Гаррисон",
    "isbn": "231231",
    "yep": 2000,
    "taken": False,
    "tbw": "-"
}, headers=headers)

#response4 = delete('http://127.0.0.1:5050/api/book/3', headers=headers)

response5 = put('http://127.0.0.1:5050/api/book/2', json=
                {"namebook": "Война и мир",
                 "name_author": "Толстой",
                 "isbn": "123123",
                 "yep": 1959,
                 "taken": True,
                 "tbw": "Илья Никулин"
                 }, headers=headers)


response6 = get('http://127.0.0.1:5050/api/book', headers=headers)

data = response6.json()

print(json.dumps(data, indent=4, ensure_ascii=False))

'''print(response4.status_code)
print(response4.text)
'''
print(response5.status_code)
print(response5.text)