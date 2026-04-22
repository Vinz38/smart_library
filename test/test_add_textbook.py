from requests import post, put, get, delete


'''response = post('http://127.0.0.1:5050/api/textbook', json={
    "itemtype": "Математика",
    "id_book": 123123123,
    "tbn": "Геометрия Углубленный Уровень",
    "yep": 2025,
    "fwc": "10 класс",
    "authors_list": "Мерзляк",
    "taken": False
})'''

'''response1 = post('http://127.0.0.1:5050/api/textbook', json={
    "itemtype": "Математика",
    "id_book": 1,
    "tbn": "Геометрия Углубленный Уровень",
    "yep": 2025,
    "fwc": "10 класс",
    "authors_list": "Мерзляк",
    "taken": False
})

response2 = post('http://127.0.0.1:5050/api/textbook', json={
    "itemtype": "Математика",
    "id_book": 2,
    "tbn": "Геометрия Углубленный Уровень",
    "yep": 2025,
    "fwc": "10 класс",
    "authors_list": "Мерзляк",
    "taken": False
})

response3 = post('http://127.0.0.1:5050/api/textbook', json={
    "itemtype": "Математика",
    "id_book": 3,
    "tbn": "Геометрия Углубленный Уровень",
    "yep": 2025,
    "fwc": "10 класс",
    "authors_list": "Мерзляк",
    "taken": False 
})'''

response4 = get('http://127.0.0.1:5050/api/textbook')

print(response4.status_code)
print(response4.text)