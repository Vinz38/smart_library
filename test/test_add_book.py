from requests import post, get
import json


response1 = post('http://127.0.0.1:8080/api/add_book', json={
    "namebook": "Повелитель мух",
    "name_author": "Уильям Голдинг",
    "isbn": "978-5-17-080086-5",
    "yep": 2023,
    "taken": False
})

response2 = post('http://127.0.0.1:8080/api/add_book', json={
    "namebook": "Война и Мир",
    "name_author": "Толстой",
    "isbn": "123123",
    "yep": 1959,
    "taken": False
})

response3 = post('http://127.0.0.1:8080/api/add_book', json={
    "namebook": "Билл герой галактики",
    "name_author": "Гарри Гаррисон",
    "isbn": "231231",
    "yep": 2000,
    "taken": False
})

response4 = get('http://127.0.0.1:8080/api/add_book')

data = response4.json()

print(json.dumps(data, indent=4, ensure_ascii=False))


print(response4.status_code)
print(response4.text)