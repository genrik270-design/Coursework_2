class Aeroplane:
    def __init__(self, icao24: str, callsign: str, origin_country: str, altitude, velocity) -> None:
        self.icao24 = icao24
        self.callsign = callsign if callsign and callsign.strip() else "Н/Д"
        self.origin_country = origin_country if origin_country else "Н/Д"
        # Создаем приватное поле по умолчанию
        self._altitude = 0.0
        self._velocity = 0.0
        # Запись через сеттеры для прохождения валидации
        self.altitude = altitude
        self.velocity = velocity

    # --- ИНКАПСУЛЯЦИЯ И ВАЛИДАЦИЯ ВЫСОТЫ И СКОРОСТИ---
    @property
    def altitude(self):
        return self._altitude

    @altitude.setter
    def altitude(self, value):
        # Если высота не указана сервером (None), ставим 0
        if value is None:
            self._altitude = 0
            return
        # Валидация: проверка типа и диапазона
        if not isinstance(value, (int, float)):
            raise ValueError("Высота должна быть числом!")
        if value < 0:
            raise ValueError("Высота не может быть отрицательной!")
        self._altitude = float(value)

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        if value is None:
            self._velocity = 0.0
            return
        if not isinstance(value, (int, float)):
            raise ValueError("Скорость должна быть числом!")
        if value < 0:
            raise ValueError("Скорость не может быть отрицательной!")
        self._velocity = float(value)

    # --- МЕТОДЫ СРАВНЕНИЯ (Сравнение по скорости) ---
    def __lt__(self, other):
        """Метод 'меньше' (<) по скорости"""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.velocity < other.velocity

    def __gt__(self, other):
        """Метод 'больше' (>) по скорости"""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.velocity > other.velocity

    def __eq__(self, other):
        """Метод 'равно' (==) по скорости"""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.velocity == other.velocity

    # --- ДОПОЛНИТЕЛЬНЫЙ МЕТОД ДЛЯ СРАВНЕНИЯ ВЫСОТЫ ---
    def compare_altitude(self, other: 'Aeroplane') -> str:
        """Сравнивает высоту двух самолетов и возвращает текстовый результат"""
        if self.altitude > other.altitude:
            return f"Самолет {self.callsign} летит ВЫШЕ, чем {other.callsign} ({self.altitude} м > {other.altitude} м)"
        elif self.altitude < other.altitude:
            return f"Самолет {self.callsign} летит НИЖЕ, чем {other.callsign} ({self.altitude} м < {other.altitude} м)"
        else:
            return f"Самолеты {self.callsign} и {other.callsign} летят на ОДНОЙ высоте ({self.altitude} м)"

    def __str__(self) -> str:
        return f"Рейс: {self.callsign:<8} | Страна: {self.origin_country:<15} | Скорость: {self.velocity:<5} м/с | Высота: {self.altitude} м"


# Проверка
if __name__ == "__main__":
    print("--- Проверка создания и валидации ---")
    # Создаем два тестовых самолета
    plane1 = Aeroplane("4b1813", "AFL2130 ", "Russian Fed.", 10200, 240.5)
    plane2 = Aeroplane("3c6625", "DLH2TC  ", "Germany", 9800, 255.2)

    print(plane1)
    print(plane2)

    print("\n--- Проверка сравнения по скорости (магические методы) ---")
    if plane1 > plane2:
        print(f"Самолет {plane1.callsign} летит быстрее.")
    elif plane1 < plane2:
        print(f"Самолет {plane2.callsign} летит быстрее.")

    print("\n--- Проверка сравнения по высоте (кастомный метод) ---")
    print(plane1.compare_altitude(plane2))

    print("\n--- Проверка работы валидации (попытка установить некорректные данные) ---")
    try:
        plane1.velocity = -50  # Вызовет ошибку
    except ValueError as e:
        print(f"Перехвачена ошибка валидации: {e}")
