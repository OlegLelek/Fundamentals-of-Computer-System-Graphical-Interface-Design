from PyQt5.QtCore import QObject, pyqtSignal

class Fahrenheit(QObject):
    # Сигнал испускается при изменении значения в градусах Фаренгейта.
    # Несёт float - новое значение в °F.
    fahrenheitChanged = pyqtSignal(float)

    ZERO_CELSIUS_IN_KELVIN = 273.15

    def __init__(self):
        super().__init__()
        self.value = 32.0 

    def set_value(self, value: float):
        """Установить новое значение в °F."""
        self.value = value
        self.fahrenheitChanged.emit(value)

    def to_kelvin(self, value: float) -> float:
        """Перевести значение из °F в Кельвины."""
        celsius = (value - 32) * 5 / 9
        return celsius + self.ZERO_CELSIUS_IN_KELVIN

    def from_kelvin(self, kelvin: float) -> float:
        """Перевести значение из Кельвинов в °F."""
        celsius = kelvin - self.ZERO_CELSIUS_IN_KELVIN
        return celsius * 9 / 5 + 32