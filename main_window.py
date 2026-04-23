import sys
import json
import os
import requests

from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt

# ---------------- LOGIN / REGISTER ----------------


class LoginWidget(QWidget):
    def __init__(self, switch_to_main):
        super().__init__()
        self.switch_to_main = switch_to_main

        main_layout = QVBoxLayout()

        # ---------------- REGISTER ----------------
        self.register_box = QGroupBox("Регистрация")
        reg_layout = QVBoxLayout()

        self.reg_inputs = {}
        reg_fields = ["Фамилия", "Имя", "Отчество",
                      "Email", "Телефон", "Пароль"]

        for f in reg_fields:
            line = QLineEdit()
            line.setPlaceholderText(f)

            if f == "Пароль":
                line.setEchoMode(QLineEdit.EchoMode.Password)

            reg_layout.addWidget(line)
            self.reg_inputs[f] = line

        self.repeat_password = QLineEdit()
        self.repeat_password.setPlaceholderText("Повторите пароль")
        self.repeat_password.setEchoMode(QLineEdit.EchoMode.Password)

        reg_layout.addWidget(self.repeat_password)

        self.register_btn = QPushButton("Зарегистрироваться")
        self.register_btn.clicked.connect(self.register)

        reg_layout.addWidget(self.register_btn)
        self.register_box.setLayout(reg_layout)

        # ---------------- LOGIN ----------------
        self.login_box = QGroupBox("Вход")
        login_layout = QVBoxLayout()

        self.login_inputs = {}
        login_fields = ["Фамилия", "Имя",
                        "Отчество", "Email", "Телефон", "Пароль"]

        for f in login_fields:
            line = QLineEdit()
            line.setPlaceholderText(f)

            if f == "Пароль":
                line.setEchoMode(QLineEdit.EchoMode.Password)

            login_layout.addWidget(line)
            self.login_inputs[f] = line

        self.login_btn = QPushButton("Войти")
        self.login_btn.clicked.connect(self.login)

        login_layout.addWidget(self.login_btn)
        self.login_box.setLayout(login_layout)

        # ---------------- SWITCH BUTTONS ----------------
        self.switch_to_login = QPushButton("Уже есть аккаунт? Войти")
        self.switch_to_register = QPushButton("Нет аккаунта? Регистрация")

        self.switch_to_login.clicked.connect(self.show_login)
        self.switch_to_register.clicked.connect(self.show_register)

        # ---------------- ADD TO MAIN ----------------
        main_layout.addWidget(self.register_box)
        main_layout.addWidget(self.login_box)
        main_layout.addWidget(self.switch_to_login)
        main_layout.addWidget(self.switch_to_register)

        self.setLayout(main_layout)

        # по умолчанию показываем регистрацию
        self.show_register()

    def show_login(self):
        self.login_box.show()
        self.register_box.hide()

    def show_register(self):
        self.login_box.hide()
        self.register_box.show()

    def register(self):
        data = {k: v.text() for k, v in self.reg_inputs.items()}
        password = data["Пароль"]
        repeat = self.repeat_password.text()

        if password != repeat:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
            return

        payload = {
            "surname": data["Фамилия"],
            "name": data["Имя"],
            "middlename": data["Отчество"],
            "email": data["Email"],
            "phonenumber": data["Телефон"],
            "password": password
        }

        try:
            r = requests.post(
                "http://127.0.0.1:5050/api/librarian", json=payload)
            QMessageBox.information(self, "Успех", "Вы зарегистрированы")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def login(self):
        data = {k: v.text() for k, v in self.login_inputs.items()}

        try:
            r = requests.get("http://127.0.0.1:5050/api/librarian")
            users = r.json()

            for u in users:
                if (
                    u.get("surname") == data["Фамилия"] and
                    u.get("name") == data["Имя"] and
                    u.get("middlename") == data["Отчество"] and
                    u.get("email") == data["Email"] and
                    u.get("phonenumber") == data["Телефон"]
                ):
                    # ⚠️ пароль надо проверять на сервере, но пока так
                    self.switch_to_main()
                    return

            QMessageBox.warning(self, "Ошибка", "Неверные данные")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))


# ---------------- ADD STUDENT DIALOG ----------------
class AddStudentDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить ученика")

        layout = QVBoxLayout()
        self.inputs = {}

        fields = ["Фамилия", "Имя", "Отчество", "Email", "Класс"]

        for f in fields:
            line = QLineEdit()
            line.setPlaceholderText(f)
            layout.addWidget(line)
            self.inputs[f] = line

        btn = QPushButton("Добавить")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)

        self.setLayout(layout)

class AddTextbookDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить учебник")

        layout = QVBoxLayout()
        self.inputs = {}

        fields = [
            "Тип",
            "Название",
            "Автор",
            "Год",
            "Класс",
            "ID книги"
        ]

        for f in fields:
            line = QLineEdit()
            line.setPlaceholderText(f)
            layout.addWidget(line)
            self.inputs[f] = line

        self.btn = QPushButton("Добавить")
        self.btn.clicked.connect(self.accept)

        layout.addWidget(self.btn)
        self.setLayout(layout)

class GiveBookDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выдать книгу")

        layout = QVBoxLayout()

        self.fio = QLineEdit()
        self.fio.setPlaceholderText("ФИО ученика")

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email ученика")

        btn = QPushButton("Выдать")
        btn.clicked.connect(self.accept)

        layout.addWidget(self.fio)
        layout.addWidget(self.email)
        layout.addWidget(btn)

        self.setLayout(layout)


class AddClassDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить класс")

        layout = QVBoxLayout()

        self.input = QLineEdit()
        self.input.setPlaceholderText("Название класса (например 10A)")

        btn = QPushButton("Сохранить")
        btn.clicked.connect(self.accept)

        layout.addWidget(self.input)
        layout.addWidget(btn)

        self.setLayout(layout)


class AddBookDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить книгу")

        layout = QVBoxLayout()
        self.inputs = {}

        fields = ["Название", "Автор", "ISBN", "Год"]

        for f in fields:
            line = QLineEdit()
            line.setPlaceholderText(f)
            layout.addWidget(line)
            self.inputs[f] = line

        btn = QPushButton("Сохранить")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)

        self.setLayout(layout)

# ---------------- CLASSES ----------------


class ClassesWidget(QWidget):
    def __init__(self, logout_callback):
        super().__init__()

        layout = QVBoxLayout()

        header = QHBoxLayout()
        self.add_class_btn = QPushButton("Добавить класс")
        self.logout_label = QLabel("<a href='#'>Выйти</a>")
        self.logout_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextBrowserInteraction)
        self.logout_label.linkActivated.connect(logout_callback)

        header.addWidget(self.add_class_btn)
        self.add_class_btn.clicked.connect(self.add_class)
        header.addStretch()
        header.addWidget(self.logout_label)

        layout.addLayout(header)

        self.combo = QComboBox()
        self.combo.currentTextChanged.connect(self.load_students)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "Фамилия", "Имя", "Отчество", "Email", "Класс", "Список книг", "Список учебников"
        ])

        self.load_classes()

        self.search = QTextBrowser()
        self.add_student_btn = QPushButton("Добавить ученика")

        layout.addWidget(self.combo)
        layout.addWidget(self.table)
        layout.addWidget(self.search)
        layout.addWidget(self.add_student_btn)

        self.setLayout(layout)

    def send_class(self, class_name):
        try:
            r = requests.post("http://127.0.0.1:5050/api/class", json={
                "class_name": class_name
            })

            print("CLASS:", r.status_code, r.text)

        except Exception as e:
            print("CLASS ERROR:", e)

    def load_classes(self):
        try:
            r = requests.get("http://127.0.0.1:5050/api/class")
            data = r.json()

            self.combo.clear()

            for c in data:
                self.combo.addItem(c["class_name"])

        except Exception as e:
            print("LOAD CLASS ERROR:", e)

    def format_books(self, data):
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except:
                return ""

        if not isinstance(data, dict):
            return ""

        result = []

        for item in data.values():
            name = item.get("namebook") or item.get("tbn") or "Без названия"
            result.append(name)

        return "\n".join(result)

    def load_students(self):
        try:
            selected_class = self.combo.currentText()

            r = requests.get("http://127.0.0.1:5050/api/users")
            data = r.json()

            table = self.table
            table.setRowCount(0)

            for user in data:
                if user.get("class_name") != selected_class:
                    continue

                row = table.rowCount()
                table.insertRow(row)

                table.setItem(row, 0, QTableWidgetItem(
                    user.get("surname", "")))
                table.setItem(row, 1, QTableWidgetItem(user.get("name", "")))
                table.setItem(row, 2, QTableWidgetItem(
                    user.get("middlename", "")))
                table.setItem(row, 3, QTableWidgetItem(user.get("email", "")))
                table.setItem(row, 4, QTableWidgetItem(
                    user.get("class_name", "")))
                books_text = self.format_books(user.get("book_list"))
                textbooks_text = self.format_books(user.get("textbook_list"))

                table.setItem(row, 5, QTableWidgetItem(books_text))
                table.setItem(row, 6, QTableWidgetItem(textbooks_text))

        except Exception as e:
            print("LOAD USERS ERROR:", e)

    def add_class(self):
        dialog = AddClassDialog()

        if dialog.exec():
            class_name = dialog.input.text()

            print("ADDING CLASS:", class_name)

            self.send_class(class_name)
            self.load_classes()

    def add_student(self):
        dialog = AddStudentDialog()
        if dialog.exec():
            row = self.table.rowCount()
            self.table.insertRow(row)

            payload = {
                "surname": dialog.inputs["Фамилия"].text(),
                "name": dialog.inputs["Имя"].text(),
                "middlename": dialog.inputs["Отчество"].text(),
                "email": dialog.inputs["Email"].text(),
                "class_name": dialog.inputs["Класс"].text()
            }

            for i, v in enumerate(payload.values()):
                self.table.setItem(row, i, QTableWidgetItem(v))

            self.table.setItem(row, 5, QTableWidgetItem(""))
            self.table.setItem(row, 6, QTableWidgetItem(""))

            self.send_user(payload)

    def send_user(self, payload):
        try:
            r = requests.post("http://127.0.0.1:5050/api/users", json=payload)
            print("USER:", r.status_code, r.text)
        except Exception as e:
            print("USER ERROR:", e)


# ---------------- BOOKS ----------------
class BooksWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels([
            "Название", "Автор", "ISBN", "Год",
            "Взята", "Кем", "Действие"
        ])

        layout.addWidget(self.table)
        self.load_books()

        bottom = QHBoxLayout()
        self.search = QTextBrowser()
        self.add_btn = QPushButton("Добавить книгу")

        bottom.addWidget(self.search)
        bottom.addWidget(self.add_btn)

        layout.addLayout(bottom)
        self.setLayout(layout)

        self.add_btn.clicked.connect(self.open_add_dialog)

    def load_books(self):
        try:
            r = requests.get("http://127.0.0.1:5050/api/book")
            data = r.json()

            self.table.setRowCount(0)

            for i, book in enumerate(data):
                self.table.insertRow(i)

                item = QTableWidgetItem(book.get("name_book", ""))
                item.setData(256, book.get("id"))
                self.table.setItem(i, 0, item)

                self.table.setItem(i, 1, QTableWidgetItem(
                    book.get("name_author", "")))
                self.table.setItem(
                    i, 2, QTableWidgetItem(book.get("isbn", "")))
                self.table.setItem(i, 3, QTableWidgetItem(
                    str(book.get("yep", ""))))
                self.table.setItem(i, 4, QTableWidgetItem(
                    str(book.get("taken", False))))
                self.table.setItem(
                    i, 5, QTableWidgetItem(book.get("tbw", "-")))

                btn = QPushButton("Выдать")
                btn.clicked.connect(lambda _, r=i: self.give_book(r))
                self.table.setCellWidget(i, 6, btn)
        except Exception as e:
            print("LOAD BOOKS ERROR:", e)

    def give_book(self, row):
        dialog = GiveBookDialog()

        if not dialog.exec():
            return

        fio = dialog.fio.text()
        email = dialog.email.text()

        # --- ищем пользователя ---
        try:
            r = requests.get("http://127.0.0.1:5050/api/users")
            users = r.json()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
            return

        user = None
        user_id = None

        for u in users:
            if u.get("email") == email:
                user = u
                user_id = u.get("id")
                break

        if not user:
            QMessageBox.warning(self, "Ошибка", "Пользователь не найден")
            return

        # --- книга ---
        book_id = self.table.item(row, 0).data(256)

        if not book_id:
            QMessageBox.warning(self, "Ошибка", "Нет ID книги")
            return

        payload = {
            "namebook": self.table.item(row, 0).text(),
            "name_author": self.table.item(row, 1).text(),
            "isbn": self.table.item(row, 2).text(),
            "yep": int(self.table.item(row, 3).text()),
            "taken": True,
            "tbw": fio
        }

        # --- обновляем книгу на сервере ---
        try:
            url = f"http://127.0.0.1:5050/api/book/{book_id}"
            r = requests.put(url, json=payload)

            print("BOOK UPDATE:", r.status_code, r.text)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка книги", str(e))
            return

        # --- обновляем пользователя (book_list) ---
        book_list = user.get("book_list", {})

        if isinstance(book_list, str):
            try:
                book_list = json.loads(book_list)
            except:
                book_list = {}

        new_key = str(len(book_list))
        book_list[new_key] = {
            "namebook": payload["namebook"],
            "tbw": fio
        }

        user_payload = {
            "surname": user.get("surname"),
            "name": user.get("name"),
            "middlename": user.get("middlename"),
            "email": user.get("email"),
            "class_name": user.get("class_name"),
            "book_list": book_list
        }

        try:
            url = f"http://127.0.0.1:5050/api/users/{user_id}"
            requests.put(url, json=user_payload)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка пользователя", str(e))
            return

        # --- обновляем UI ---
        self.table.setItem(row, 4, QTableWidgetItem("True"))
        self.table.setItem(row, 5, QTableWidgetItem(fio))

        QMessageBox.information(self, "Успех", "Книга выдана")

    def open_add_dialog(self):
        dialog = AddBookDialog()
        if dialog.exec():
            row = self.table.rowCount()
            self.table.insertRow(row)

            payload = {
                "namebook": dialog.inputs["Название"].text(),
                "name_author": dialog.inputs["Автор"].text(),
                "isbn": dialog.inputs["ISBN"].text(),
                "yep": dialog.inputs["Год"].text(),
                "taken": False,
                "tbw": "-"
            }

            self.fill_row(row, payload)
            self.send_book(payload)

    def fill_row(self, row, p):
        self.table.setItem(row, 0, QTableWidgetItem(p["namebook"]))
        self.table.item(row, 0).setData(256, p.get("id"))
        self.table.setItem(row, 1, QTableWidgetItem(p["namebook"]))
        self.table.setItem(row, 2, QTableWidgetItem(p["name_author"]))
        self.table.setItem(row, 3, QTableWidgetItem(p["isbn"]))
        self.table.setItem(row, 4, QTableWidgetItem(str(p["yep"])))
        self.table.setItem(row, 5, QTableWidgetItem("Нет"))
        self.table.setItem(row, 6, QTableWidgetItem("-"))

        btn = QPushButton("Выдать")
        btn.clicked.connect(lambda _, r=row: self.give_book(r))
        self.table.setCellWidget(row, 6, btn)

    def send_book(self, payload):
        try:
            r = requests.post("http://127.0.0.1:5050/api/book", json=payload)
            print("BOOK:", r.status_code, r.text)
        except Exception as e:
            print("BOOK ERROR:", e)


# ---------------- TEXTBOOKS ----------------
class TextbooksWidget(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        # ---------------- SEARCH ----------------
        search_box = QGroupBox("Поиск учебников")
        search_layout = QGridLayout()

        self.search_inputs = {}

        fields = [
            ("Тип", "itemtype"),
            ("Название", "tbn"),
            ("Автор", "authors_list"),
            ("Год", "yep"),
            ("Класс", "fwc"),
            ("ID книги", "id_book")
        ]

        for i, (label, key) in enumerate(fields):
            search_layout.addWidget(QLabel(label), i, 0)
            line = QLineEdit()
            search_layout.addWidget(line, i, 1)
            self.search_inputs[key] = line

        self.search_btn = QPushButton("Поиск")
        self.search_btn.clicked.connect(self.search_textbooks)

        search_layout.addWidget(self.search_btn, len(fields), 0, 1, 2)
        search_box.setLayout(search_layout)

        # ---------------- TABLE ----------------
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "Тип", "Название", "Автор", "Год", "Класс", "ID"
        ])

        # ---------------- BUTTON ----------------
        self.add_btn = QPushButton("Добавить учебник")
        self.add_btn.clicked.connect(self.open_add_dialog)

        main_layout.addWidget(search_box)
        main_layout.addWidget(self.add_btn)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

        self.load_textbooks()

    # ---------------- LOAD ----------------
    def load_textbooks(self):
        try:
            r = requests.get("http://127.0.0.1:5050/api/textbook")
            data = r.json()

            self.table.setRowCount(0)

            for i, tb in enumerate(data):
                self.table.insertRow(i)

                self.table.setItem(
                    i, 0, QTableWidgetItem(tb.get("itemtype", "")))
                self.table.setItem(i, 1, QTableWidgetItem(tb.get("tbn", "")))
                self.table.setItem(i, 2, QTableWidgetItem(
                    tb.get("authors_list", "")))
                self.table.setItem(
                    i, 3, QTableWidgetItem(str(tb.get("yep", ""))))
                self.table.setItem(i, 4, QTableWidgetItem(tb.get("fwc", "")))
                self.table.setItem(i, 5, QTableWidgetItem(
                    str(tb.get("id_book", ""))))

        except Exception as e:
            print("LOAD TEXTBOOKS ERROR:", e)

    # ---------------- ADD ----------------
    def open_add_dialog(self):
        dialog = AddTextbookDialog()

        if dialog.exec():
            try:
                payload = {
                    "itemtype": dialog.inputs["Тип"].text(),
                    "tbn": dialog.inputs["Название"].text(),
                    "authors_list": dialog.inputs["Автор"].text(),
                    "yep": int(dialog.inputs["Год"].text()),
                    "fwc": dialog.inputs["Класс"].text(),
                    "id_book": int(dialog.inputs["ID книги"].text()),
                    "taken": False
                }

                r = requests.post(
                    "http://127.0.0.1:5050/api/textbook",
                    json=payload
                )

                print("TEXTBOOK:", r.status_code, r.text)

                if r.status_code == 200:
                    QMessageBox.information(self, "OK", "Учебник добавлен")
                    self.load_textbooks()
                else:
                    QMessageBox.critical(self, "Ошибка", r.text)

            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Год и ID должны быть числами")

    # ---------------- GIVE ----------------
    def give_textbook(self, row):
        dialog = GiveBookDialog()

        if not dialog.exec():
            return

        fio = dialog.fio.text()
        email = dialog.email.text()

        # --- user search ---
        try:
            r = requests.get("http://127.0.0.1:5050/api/users")
            users = r.json()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
            return

        user = None
        user_id = None

        for u in users:
            if u.get("email") == email:
                user = u
                user_id = u.get("id")
                break

        if not user:
            QMessageBox.warning(self, "Ошибка", "Пользователь не найден")
            return

        # --- textbook ---
        id_book = self.table.item(row, 1).data(256)

        if not id_book:
            QMessageBox.warning(self, "Ошибка", "Нет ID учебника")
            return

        payload = {
            "itemtype": self.table.item(row, 0).text(),
            "tbn": self.table.item(row, 1).text(),
            "yep": int(self.table.item(row, 3).text()),
            "fwc": self.table.item(row, 4).text(),
            "id_book": id_book,
            "authors_list": self.table.item(row, 2).text(),
            "taken": True,
            "tbw": fio
        }

        # --- update textbook ---
        try:
            url = f"http://127.0.0.1:5050/api/textbook/{id_book}"
            r = requests.put(url, json=payload)

            print("TEXTBOOK GIVE:", r.status_code, r.text)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
            return

        # --- update user textbook_list ---
        textbook_list = user.get("textbook_list", {})

        if isinstance(textbook_list, str):
            try:
                textbook_list = json.loads(textbook_list)
            except:
                textbook_list = {}

        new_key = str(len(textbook_list))
        textbook_list[new_key] = {
            "tbn": payload["tbn"],
            "tbw": fio
        }

        user_payload = {
            "surname": user.get("surname"),
            "name": user.get("name"),
            "middlename": user.get("middlename"),
            "email": user.get("email"),
            "class_name": user.get("class_name"),
            "textbook_list": textbook_list
        }

        try:
            url = f"http://127.0.0.1:5050/api/users/{user_id}"
            requests.put(url, json=user_payload)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка пользователя", str(e))
            return

        # --- update UI ---
        self.table.setItem(row, 5, QTableWidgetItem("True"))
        self.table.setItem(row, 6, QTableWidgetItem(fio))

        QMessageBox.information(self, "Успех", "Учебник выдан")

    def search_textbooks(self):
        query = {
            k: v.text().lower()
            for k, v in self.search_inputs.items()
        }

        try:
            r = requests.get("http://127.0.0.1:5050/api/textbook")
            data = r.json()

            self.table.setRowCount(0)

            for tb in data:
                if query["itemtype"] and query["itemtype"] not in tb.get("itemtype", "").lower():
                    continue
                if query["tbn"] and query["tbn"] not in tb.get("tbn", "").lower():
                    continue
                if query["authors_list"] and query["authors_list"] not in tb.get("authors_list", "").lower():
                    continue
                if query["fwc"] and query["fwc"] not in tb.get("fwc", "").lower():
                    continue
                if query["id_book"] and query["id_book"] != str(tb.get("id_book", "")):
                    continue

                row = self.table.rowCount()
                self.table.insertRow(row)

                self.table.setItem(row, 0, QTableWidgetItem(tb.get("itemtype", "")))
                self.table.setItem(row, 1, QTableWidgetItem(tb.get("tbn", "")))
                self.table.setItem(row, 2, QTableWidgetItem(tb.get("authors_list", "")))
                self.table.setItem(row, 3, QTableWidgetItem(str(tb.get("yep", ""))))
                self.table.setItem(row, 4, QTableWidgetItem(tb.get("fwc", "")))
                self.table.setItem(row, 5, QTableWidgetItem(str(tb.get("id_book", ""))))

        except Exception as e:
            print("SEARCH ERROR:", e)

# ---------------- MAIN ----------------


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Библиотека")
        self.resize(1200, 800)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        '''self.login = LoginWidget(self.show_main)
        self.stack.addWidget(self.login)
        '''
        self.main_widget = QWidget()
        self.stack.addWidget(self.main_widget)

        self.init_main()

    def init_main(self):
        layout = QHBoxLayout()

        self.combo = QComboBox()
        self.combo.addItems(["Классы", "Книги", "Учебники"])

        self.group = QGroupBox("Содержимое")
        self.group_layout = QVBoxLayout()
        self.group.setLayout(self.group_layout)

        layout.addWidget(self.combo)
        layout.addWidget(self.group)

        self.main_widget.setLayout(layout)

        self.classes = ClassesWidget(self.logout)
        self.books = BooksWidget()
        self.textbooks = TextbooksWidget()

        self.combo.currentIndexChanged.connect(self.switch_view)
        self.switch_view(0)

    def switch_view(self, i):
        for j in reversed(range(self.group_layout.count())):
            self.group_layout.itemAt(j).widget().setParent(None)

        self.group_layout.addWidget(
            [self.classes, self.books, self.textbooks][i])

    def show_main(self):
        self.stack.setCurrentIndex(1)

    def logout(self):
        self.stack.setCurrentIndex(0)


# ---------------- RUN ----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
