import sys
import secrets
import string
import pyperclip
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QSpinBox, QCheckBox, 
    QPushButton, QLineEdit, QGroupBox, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon


class PasswordGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Генератор надежных паролей")
        self.setFixedSize(600, 550)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        
        # Заголовок
        title_label = QLabel("Генератор паролей")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Группа настроек
        settings_group = QGroupBox("Настройки пароля")
        settings_layout = QVBoxLayout()
        
        # Длина пароля
        length_layout = QHBoxLayout()
        length_label = QLabel("Длина пароля:")
        self.length_spinbox = QSpinBox()
        self.length_spinbox.setRange(8, 64)
        self.length_spinbox.setValue(16)
        length_layout.addWidget(length_label)
        length_layout.addWidget(self.length_spinbox)
        length_layout.addStretch()
        settings_layout.addLayout(length_layout)
        
        # Типы символов
        self.lowercase_check = QCheckBox("Строчные буквы (a-z)")
        self.lowercase_check.setChecked(True)
        settings_layout.addWidget(self.lowercase_check)
        
        self.uppercase_check = QCheckBox("Заглавные буквы (A-Z)")
        self.uppercase_check.setChecked(True)
        settings_layout.addWidget(self.uppercase_check)
        
        self.digits_check = QCheckBox("Цифры (0-9)")
        self.digits_check.setChecked(True)
        settings_layout.addWidget(self.digits_check)
        
        self.symbols_check = QCheckBox("Специальные символы (!@#$%^&*)")
        self.symbols_check.setChecked(True)
        settings_layout.addWidget(self.symbols_check)
        
        settings_group.setLayout(settings_layout)
        main_layout.addWidget(settings_group)
        
        # Поле для отображения пароля
        password_layout = QVBoxLayout()
        password_label = QLabel("Сгенерированный пароль:")
        password_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        password_layout.addWidget(password_label)
        
        self.password_display = QLineEdit()
        self.password_display.setReadOnly(True)
        self.password_display.setMinimumHeight(40)
        self.password_display.setFont(QFont("Courier", 12))
        password_layout.addWidget(self.password_display)
        
        main_layout.addLayout(password_layout)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        
        self.generate_btn = QPushButton("Сгенерировать")
        self.generate_btn.clicked.connect(self.generate_password)
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        self.copy_btn = QPushButton("Копировать")
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        self.copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        
        self.clear_btn = QPushButton("Очистить")
        self.clear_btn.clicked.connect(self.clear_password)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        
        buttons_layout.addWidget(self.generate_btn)
        buttons_layout.addWidget(self.copy_btn)
        buttons_layout.addWidget(self.clear_btn)
        main_layout.addLayout(buttons_layout)
        
        # Индикатор надежности
        self.security_label = QLabel("")
        self.security_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.security_label.setFont(QFont("Arial", 10))
        main_layout.addWidget(self.security_label)
        
        # Информация
        info_label = QLabel(
            "💡 Советы по безопасности:\n"
            "• Используйте пароли длиной от 12 символов\n"
            "• Включайте разные типы символов\n"
            "• Не используйте один пароль для разных сервисов\n"
            "• Регулярно меняйте важные пароли"
        )
        info_label.setStyleSheet("""
            QLabel {
                background-color: #00000;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #bbdefb;
            }
        """)
        info_label.setWordWrap(True)
        main_layout.addWidget(info_label)
        
        # Статусная строка
        self.status_label = QLabel("Готов к генерации пароля")
        self.statusBar().addWidget(self.status_label)
        
        # Генерируем первый пароль
        self.generate_password()

    def generate_password(self):
        """Генерирует пароль на основе выбранных настроек"""
        # Собираем доступные символы
        characters = ''
        
        if self.lowercase_check.isChecked():
            characters += string.ascii_lowercase
        if self.uppercase_check.isChecked():
            characters += string.ascii_uppercase
        if self.digits_check.isChecked():
            characters += string.digits
        if self.symbols_check.isChecked():
            characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Проверяем, что выбран хотя бы один тип символов
        if not characters:
            QMessageBox.warning(self, "Ошибка", 
                              "Выберите хотя бы один тип символов!")
            return
        
        # Проверяем минимальную длину
        length = self.length_spinbox.value()
        if length < 8:
            QMessageBox.warning(self, "Предупреждение", 
                              "Рекомендуется использовать пароли длиной не менее 8 символов!")
        
        # Генерируем пароль
        try:
            password = ''.join(secrets.choice(characters) for _ in range(length))
            self.password_display.setText(password)
            self.update_security_indicator(password)
            self.status_label.setText("Пароль сгенерирован")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сгенерировать пароль: {str(e)}")

    def update_security_indicator(self, password):
        """Обновляет индикатор надежности пароля"""
        length = len(password)
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(not c.isalnum() for c in password)
        
        score = 0
        if length >= 12:
            score += 2
        elif length >= 8:
            score += 1
            
        score += has_lower + has_upper + has_digit + has_symbol
        
        if score >= 6:
            color = "#4CAF50"
            text = "Отличный пароль 🔒"
        elif score >= 4:
            color = "#FFC107"
            text = "Хороший пароль 👍"
        else:
            color = "#F44336"
            text = "Слабый пароль ⚠️"
        
        self.security_label.setText(text)
        self.security_label.setStyleSheet(f"color: {color}; font-weight: bold;")

    def copy_to_clipboard(self):
        """Копирует пароль в буфер обмена"""
        password = self.password_display.text()
        if password:
            try:
                pyperclip.copy(password)
                self.status_label.setText("Пароль скопирован в буфер обмена")
                
                # Показываем временное сообщение
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Успех")
                msg.setText("Пароль скопирован в буфер обмена!")
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", 
                                   f"Не удалось скопировать в буфер обмена: {str(e)}")
        else:
            QMessageBox.warning(self, "Предупреждение", "Сначала сгенерируйте пароль!")

    def clear_password(self):
        """Очищает поле с паролем"""
        self.password_display.clear()
        self.security_label.clear()
        self.status_label.setText("Поле очищено")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Устанавливаем тему
    app.setStyleSheet("""
        QMainWindow {
            background-color: #00000;
        }
        QGroupBox {
            font-weight: bold;
            border: 2px solid #00000;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        QLineEdit {
            padding: 5px;
            border: 2px solid #00000;
            border-radius: 5px;
            background-color: #00000;
        }
        QSpinBox {
            padding: 5px;
            border: 1px solid #00000;
            border-radius: 3px;
        }
    """)
    
    window = PasswordGenerator()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()