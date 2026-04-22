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

        layout = QVBoxLayout()

        self.inputs = {}
        fields = ["Фамилия", "Имя", "Отчество", "Email", "Телефон"]

        for f in fields:
            line = QLineEdit()
            line.setPlaceholderText(f)
            layout.addWidget(line)
            self.inputs[f] = line

        self.login_btn = QPushButton("Войти")
        self.register_btn = QPushButton("Регистрация")

        self.login_btn.clicked.connect(self.login)

        layout.addWidget(self.login_btn)
        layout.addWidget(self.register_btn)

        self.setLayout(layout)

    def login(self):
        self.switch_to_main()


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


class GiveBookDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выдать книгу ученику")

        layout = QVBoxLayout()

        self.input = QLineEdit()
        self.input.setPlaceholderText("ФИО ученика")

        self.btn = QPushButton("Выдать")
        self.btn.clicked.connect(self.accept)

        layout.addWidget(self.input)
        layout.addWidget(self.btn)

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
        self.load_classes()

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels([
            "Фамилия", "Имя", "Отчество", "Email", "Класс"
        ])

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

                self.table.setItem(i, 0, QTableWidgetItem(
                    book.get("namebook", "")))
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

                self.table.setCellWidget(i, 6, QPushButton("Выдать"))

        except Exception as e:
            print("LOAD BOOKS ERROR:", e)

    def give_book(self, row):
        dialog = GiveBookDialog()

        if dialog.exec():
            student = dialog.input.text()

            namebook = self.table.item(row, 0).text()
            author = self.table.item(row, 1).text()
            isbn = self.table.item(row, 2).text()
            year = int(self.table.item(row, 3).text())

            book_id = self.table.item(row, 0).data(256)

            payload = {
                "namebook": namebook,
                "name_author": author,
                "isbn": isbn,
                "yep": year,
                "taken": True,
                "tbw": student
            }

            try:
                url = f"http://127.0.0.1:5050/api/book/{book_id}"
                r = requests.put(url, json=payload)

                print("GIVE BOOK:", r.status_code, r.text)

                self.table.setItem(row, 4, QTableWidgetItem("Да"))
                self.table.setItem(row, 5, QTableWidgetItem(student))

            except Exception as e:
                print("ERROR GIVE BOOK:", e)

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
class TextbooksWidget(BooksWidget):
    def load_textbooks(self):
        try:
            r = requests.get("http://127.0.0.1:5050/api/textbook")
            data = r.json()

            self.table.setRowCount(0)

            for i, book in enumerate(data):
                self.table.insertRow(i)

                self.table.setItem(i, 0, QTableWidgetItem(book.get("tbn", "")))
                self.table.setItem(i, 1, QTableWidgetItem(
                    book.get("authors_list", "")))
                self.table.setItem(i, 2, QTableWidgetItem(
                    str(book.get("id_book", ""))))
                self.table.setItem(i, 3, QTableWidgetItem(
                    str(book.get("yep", ""))))
                self.table.setItem(i, 4, QTableWidgetItem(
                    str(book.get("taken", False))))
                self.table.setItem(i, 5, QTableWidgetItem(book.get("fwc", "")))

                self.table.setCellWidget(i, 6, QPushButton("Выдать"))

        except Exception as e:
            print("LOAD TEXTBOOKS ERROR:", e)

    def open_add_dialog(self):
        dialog = AddBookDialog()
        if dialog.exec():
            row = self.table.rowCount()
            self.table.insertRow(row)

            payload = {
                "itemtype": dialog.inputs["Название"].text(),
                "id_book": int(dialog.inputs["ISBN"].text()) if dialog.inputs["ISBN"].text().isdigit() else 0,
                "tbn": dialog.inputs["Название"].text(),
                "yep": int(dialog.inputs["Год"].text()) if dialog.inputs["Год"].text().isdigit() else 0,
                "fwc": "",
                "authors_list": dialog.inputs["Автор"].text(),
                "taken": False
            }

            self.fill_row(row, {
                "namebook": payload["tbn"],
                "name_author": payload["authors_list"],
                "isbn": payload["id_book"],
                "yep": payload["yep"]
            })

            self.send_textbook(payload)

    def send_textbook(self, payload):
        try:
            r = requests.post(
                "http://127.0.0.1:5050/api/textbook", json=payload)
            print("TEXTBOOK:", r.status_code, r.text)
        except Exception as e:
            print("TEXTBOOK ERROR:", e)


# ---------------- MAIN ----------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Библиотека")
        self.resize(1200, 800)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # self.login = LoginWidget(self.show_main)
        # self.stack.addWidget(self.login)

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
