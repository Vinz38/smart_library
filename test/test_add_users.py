from requests import post


response = post('http://127.0.0.1:8080/api/add_users', json={
    "surname": "Никулин",
    "name": "Илья",
    "middlename": "Алексеевич",
    "email": "ilia.nikulin09@gmail.com"
})

print(response.status_code)
print(response.text)