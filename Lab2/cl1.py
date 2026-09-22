from PyQt5.QtCore import QObject, pyqtSignal

class Celsius(QObject):
    # Сигнал испускается при изменении значения в градусах Цельсия.
    # Несёт float - новое значение в °C.
    celsiusChanged = pyqtSignal(float)

    ZERO_CELSIUS_IN_KELVIN = 273.15

    def __init__(self):
        super().__init__()
        self.value = 0.0  

    def set_value(self, value: float):
        """Установить новое значение в °C"""
        self.value = value
        self.celsiusChanged.emit(value)

    def to_kelvin(self, value: float) -> float:
        """Перевести значение из °C в Кельвины."""
        return value + self.ZERO_CELSIUS_IN_KELVIN

    def from_kelvin(self, kelvin: float) -> float:
        """Перевести значение из Кельвинов в °C."""
        return kelvin - self.ZERO_CELSIUS_IN_KELVIN


def func():
    newOne = Celsius()
    newOne.set_value(25.0)
    print("Celsius:", newOne.value, "-> Kelvin:", newOne.to_kelvin(newOne.value))


if __name__ == "__main__":
    func()