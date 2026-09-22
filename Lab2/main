import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit,
    QVBoxLayout, QHBoxLayout
)
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import Qt

import cl1
import cl2


class Some(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная работа №2 - Конвертер температуры")
        self.setFixedSize(360, 220)

        # Создаём объекты классов с сигналами из cl1 и cl2
        self.celsius = cl1.Celsius()
        self.fahrenheit = cl2.Fahrenheit()

        self.updating = False

        central = QWidget()
        self.setCentralWidget(central)

        # Поле "Цельсий" 
        self.c_label = QLabel("Цельсий (°C):")
        self.c_input = QLineEdit()
        self.c_input.setValidator(QDoubleValidator(-273.15, 1e6, 2))
        self.c_input.setText("0")

        # Поле "Фаренгейт" 
        self.f_label = QLabel("Фаренгейт (°F):")
        self.f_input = QLineEdit()
        self.f_input.setValidator(QDoubleValidator(-459.67, 1e6, 2))

        # Поле "Кельвин" 
        self.k_label = QLabel("Кельвин (K):")
        self.k_input = QLineEdit()
        self.k_input.setValidator(QDoubleValidator(0.0, 1e6, 2))

        layout = QVBoxLayout()
        for label, field in (
            (self.c_label, self.c_input),
            (self.f_label, self.f_input),
            (self.k_label, self.k_input),
        ):
            row = QHBoxLayout()
            row.addWidget(label)
            row.addWidget(field)
            layout.addLayout(row)

        hint = QLabel("Формулы: °F = °C×9/5+32,  K = °C+273.15")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet("color: gray; font-size: 11px;")
        layout.addWidget(hint)

        central.setLayout(layout)

        # Подключение сигналов виджетов к слотам окна
        self.c_input.textChanged.connect(self.on_celsius_changed)
        self.f_input.textChanged.connect(self.on_fahrenheit_changed)
        self.k_input.textChanged.connect(self.on_kelvin_changed)

        # Подключение кастомных сигналов классов cl1/cl2 к слотам окна 
        self.celsius.celsiusChanged.connect(self.on_model_celsius_changed)
        self.fahrenheit.fahrenheitChanged.connect(self.on_model_fahrenheit_changed)

        # Инициализация полей на основе стартового значения в Цельсиях
        self.on_celsius_changed(self.c_input.text())

    # Слоты интерфейса
    def on_celsius_changed(self, text: str):
        """Слот: пользователь изменил поле °C."""
        if self.updating:
            return
        value = self._to_float(text)
        kelvin = self.celsius.to_kelvin(value)
        self._update_all(kelvin, skip="C")
        self.celsius.set_value(value)

    def on_fahrenheit_changed(self, text: str):
        """Слот: пользователь изменил поле °F."""
        if self.updating:
            return
        value = self._to_float(text)
        kelvin = self.fahrenheit.to_kelvin(value)
        self._update_all(kelvin, skip="F")
        self.fahrenheit.set_value(value)

    def on_kelvin_changed(self, text: str):
        """Слот: пользователь изменил поле K."""
        if self.updating:
            return
        kelvin = self._to_float(text)
        self._update_all(kelvin, skip="K")

    # Слоты, подключённые к кастомным сигналам cl1/cl2
    def on_model_celsius_changed(self, value: float):
        """Слот, реагирующий на сигнал celsiusChanged класса Celsius."""
        pass  

    def on_model_fahrenheit_changed(self, value: float):
        """Слот, реагирующий на сигнал fahrenheitChanged класса Fahrenheit."""
        pass

    # Вспомогательные методы 
    def _to_float(self, text: str) -> float:
        text = text.replace(",", ".").strip()
        try:
            return float(text) if text else 0.0
        except ValueError:
            return 0.0

    def _update_all(self, kelvin_value: float, skip: str):
        """Обновляет все три поля на основе значения в Кельвинах."""
        self.updating = True

        if skip != "C":
            c_value = self.celsius.from_kelvin(kelvin_value)
            self.c_input.setText(f"{c_value:.2f}")
        if skip != "F":
            f_value = self.fahrenheit.from_kelvin(kelvin_value)
            self.f_input.setText(f"{f_value:.2f}")
        if skip != "K":
            self.k_input.setText(f"{kelvin_value:.2f}")

        self.updating = False


if __name__ == "__main__":
    cl1.func() 
    app = QApplication(sys.argv)
    window = Some()
    window.show()
    app.exec_()
