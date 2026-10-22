import sys

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel,
    QLineEdit, QPushButton, QRadioButton, QCheckBox,
    QTextEdit, QVBoxLayout, QHBoxLayout, QComboBox,
    QListWidget, QGroupBox, QMessageBox
)


class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Task Manager 2.0")
        self.resize(700, 800)

        # Список для хранения задач
        self.tasks = []

        # Центральный виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Название задачи
        self.task_label = QLabel("Название задачи:")
        self.task_edit = QLineEdit()
        self.task_edit.setPlaceholderText("Введите название задачи")

        # Счётчик символов
        self.characters_label = QLabel("Название: 0 символов")

        # Описание задачи
        self.description_label = QLabel("Описание:")
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText(
            "Введите описание задачи"
        )

        # Приоритет задачи
        self.priority_label = QLabel("Приоритет:")

        self.low_radio = QRadioButton("Low")
        self.medium_radio = QRadioButton("Medium")
        self.high_radio = QRadioButton("High")

        # Дополнительные настройки
        self.important_check = QCheckBox("Important")
        self.notification_check = QCheckBox("Send notification")
        self.favorite_check = QCheckBox("Add to favorites")

        # Кнопки
        self.create_button = QPushButton("Добавить задачу")
        self.clear_button = QPushButton("Очистить список")
        self.delete_button = QPushButton("Удалить последнюю задачу")

        # Статус и счётчик задач
        self.status_label = QLabel("Задач: 0")
        self.count_label = QLabel("Создано задач: 0")

        # Фильтр по приоритету
        self.filter_label = QLabel("Фильтр по приоритету:")
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All", "Low", "Medium", "High"])

        # Список задач
        self.task_list_label = QLabel("Созданные задачи:")
        self.task_list = QListWidget()

        # Основной вертикальный layout
        main_layout = QVBoxLayout()

        # Строка названия
        task_layout = QHBoxLayout()
        task_layout.addWidget(self.task_label)
        task_layout.addWidget(self.task_edit)

        # Группа приоритетов
        priority_group = QGroupBox("Выберите приоритет")
        priority_layout = QHBoxLayout()
        priority_layout.addWidget(self.low_radio)
        priority_layout.addWidget(self.medium_radio)
        priority_layout.addWidget(self.high_radio)
        priority_group.setLayout(priority_layout)

        # Строка фильтра
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(self.filter_label)
        filter_layout.addWidget(self.filter_combo)

        # Строка кнопок
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.create_button)
        buttons_layout.addWidget(self.clear_button)
        buttons_layout.addWidget(self.delete_button)

        # Добавление элементов в основной layout
        main_layout.addWidget(self.task_label)
        main_layout.addLayout(task_layout)
        main_layout.addWidget(self.characters_label)
        main_layout.addWidget(self.description_label)
        main_layout.addWidget(self.description_edit)
        main_layout.addWidget(priority_group)
        main_layout.addWidget(self.important_check)
        main_layout.addWidget(self.notification_check)
        main_layout.addWidget(self.favorite_check)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.count_label)
        main_layout.addLayout(filter_layout)
        main_layout.addWidget(self.task_list_label)
        main_layout.addWidget(self.task_list)

        self.central_widget.setLayout(main_layout)

        # Подключение сигналов
        self.create_button.clicked.connect(self.create_task)
        self.clear_button.clicked.connect(self.clear_list)
        self.delete_button.clicked.connect(self.delete_last_task)
        self.filter_combo.currentTextChanged.connect(self.show_tasks)
        self.task_edit.textChanged.connect(self.update_character_count)

        # Оформление интерфейса
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFF0F5;
            }

            QLabel {
                color: #B84D78;
                font-size: 14px;
            }

            QLineEdit, QTextEdit {
                background-color: white;
                color: #444444;
                border: 1px solid #F2A7C0;
                border-radius: 8px;
                padding: 7px;
                font-size: 14px;
            }

            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #E879A5;
            }

            QRadioButton, QCheckBox {
                color: #B84D78;
                spacing: 6px;
                font-size: 14px;
            }

            QGroupBox {
                color: #B84D78;
                border: 1px solid #F2A7C0;
                border-radius: 8px;
                margin-top: 10px;
                padding: 10px;
                font-size: 14px;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 4px;
            }

            QPushButton {
                background-color: #F2A7C0;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 9px;
                font-size: 13px;
            }

            QPushButton:hover {
                background-color: #E879A5;
            }

            QPushButton:pressed {
                background-color: #D95D8B;
            }

            QComboBox {
                background-color: white;
                color: #444444;
                border: 1px solid #F2A7C0;
                border-radius: 6px;
                padding: 6px;
            }

            QListWidget {
                background-color: white;
                color: #444444;
                border: 1px solid #F2A7C0;
                border-radius: 8px;
                padding: 5px;
                font-size: 13px;
            }

            QListWidget::item {
                padding: 7px;
                border-bottom: 1px solid #FCE1EA;
            }

            QListWidget::item:selected {
                background-color: #FCE1EA;
                color: #A83E68;
            }
        """)

    def create_task(self):
        # Получение данных из полей
        name = self.task_edit.text().strip()
        description = self.description_edit.toPlainText().strip()

        # Проверка названия
        if not name:
            QMessageBox.warning(
                self, "Ошибка", "Введите название задачи."
            )
            self.task_edit.setFocus()
            return

        # Проверка выбранного приоритета
        if self.low_radio.isChecked():
            priority = "Low"
        elif self.medium_radio.isChecked():
            priority = "Medium"
        elif self.high_radio.isChecked():
            priority = "High"
        else:
            QMessageBox.warning(
                self, "Ошибка", "Выберите приоритет задачи."
            )
            return

        # Получение дополнительных настроек
        important = self.important_check.isChecked()
        notification = self.notification_check.isChecked()
        favorite = self.favorite_check.isChecked()

        # Создание словаря с данными задачи
        task = {
            "name": name,
            "description": description,
            "priority": priority,
            "important": important,
            "notification": notification,
            "favorite": favorite
        }

        # Сохранение задачи в список
        self.tasks.append(task)

        # Обновление интерфейса
        self.show_tasks()
        self.update_task_count()
        self.status_label.setText(
            f"Задач: {len(self.tasks)}"
        )

        # Вывод информации в консоль
        print("Task created:")
        print(f"Task: {name}")
        print(f"Description: {description}")
        print(f"Priority: {priority}")
        print(f"Important: {'Yes' if important else 'No'}")
        print(f"Send notification: {'Yes' if notification else 'No'}")
        print(f"Favorite: {'Yes' if favorite else 'No'}")
        print("-" * 30)

        # Очистка формы после добавления
        self.clear_form()

    def show_tasks(self):
        # Получение выбранного фильтра
        selected_filter = self.filter_combo.currentText()

        self.task_list.clear()

        # Отображение задач с учётом фильтра
        for task in self.tasks:
            if (
                selected_filter != "All"
                and task["priority"] != selected_filter
            ):
                continue

            task_text = (
                f'{task["name"]} | Priority: {task["priority"]}'
            )

            if task["important"]:
                task_text += " | Important"

            if task["favorite"]:
                task_text += " | Favorite"

            self.task_list.addItem(task_text)

    def update_character_count(self, text):
        # Подсчёт символов в названии
        count = len(text)
        self.characters_label.setText(
            f"Название: {count} символов"
        )

    def update_task_count(self):
        # Обновление количества созданных задач
        self.count_label.setText(
            f"Создано задач: {len(self.tasks)}"
        )

    def clear_form(self):
        # Очистка полей формы
        self.task_edit.clear()
        self.description_edit.clear()

        # Сброс выбранного приоритета
        self.low_radio.setAutoExclusive(False)
        self.medium_radio.setAutoExclusive(False)
        self.high_radio.setAutoExclusive(False)

        self.low_radio.setChecked(False)
        self.medium_radio.setChecked(False)
        self.high_radio.setChecked(False)

        self.low_radio.setAutoExclusive(True)
        self.medium_radio.setAutoExclusive(True)
        self.high_radio.setAutoExclusive(True)

        # Сброс флажков
        self.important_check.setChecked(False)
        self.notification_check.setChecked(False)
        self.favorite_check.setChecked(False)

    def clear_list(self):
        # Проверка наличия задач
        if not self.tasks:
            QMessageBox.information(
                self, "Информация", "Список задач уже пуст."
            )
            return

        # Подтверждение очистки
        answer = QMessageBox.question(
            self,
            "Подтверждение",
            "Вы действительно хотите очистить список задач?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        # Очистка только после подтверждения
        if answer == QMessageBox.StandardButton.Yes:
            self.tasks.clear()
            self.show_tasks()
            self.update_task_count()
            self.status_label.setText("Задач: 0")

    def delete_last_task(self):
        # Проверка наличия задач
        if not self.tasks:
            QMessageBox.information(
                self, "Информация", "Нет задач для удаления."
            )
            return

        # Удаление последней созданной задачи
        self.tasks.pop()

        self.show_tasks()
        self.update_task_count()
        self.status_label.setText(
            f"Задач: {len(self.tasks)}"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = TaskManager()
    window.show()

    sys.exit(app.exec())
