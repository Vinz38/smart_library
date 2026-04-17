from requests import post


response = post('http://127.0.0.1:8080/api/add_textbook', json={
    "itemtype": "Математика",
    "tbn": "Геометрия Углубленный Уровень",
    "yep": 2025,
    "id_book": 123123123,
    "authors_list": "Мерзляк, и т.д."
})

print(response.status_code)
print(response.text)