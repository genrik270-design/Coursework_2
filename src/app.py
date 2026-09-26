class Aeroplane:
    def __init__(self, icao24: str, callsign: str, origin_country: str, altitude, velocity) -> None:
        self.icao24 = icao24
        self.callsign = callsign if callsign and callsign.strip() else "Н/Д"
        self.origin_country = origin_country if origin_country else "Н/Д"
        self.altitude = altitude
        self.velocity = velocity

    @property
    def altitude(self):
        return self._altitude

    @altitude.setter
    def altitude(self, value):
        if value is None:
            self._altitude = 0.0
            return
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

    def __lt__(self, other):
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.velocity < other.velocity

    def __gt__(self, other):
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.velocity > other.velocity

    def __eq__(self, other):
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.velocity == other.velocity

    def compare_altitude(self, other: 'Aeroplane') -> str:
        if self.altitude > other.altitude:
            return f"Самолет {self.callsign.strip()} летит ВЫШЕ, чем {other.callsign.strip()} ({self.altitude} м > {other.altitude} м)"
        elif self.altitude < other.altitude:
            return f"Самолет {self.callsign.strip()} летит НИЖЕ, чем {other.callsign.strip()} ({self.altitude} м < {other.altitude} м)"
        else:
            return f"Самолеты {self.callsign.strip()} и {other.callsign.strip()} летят на ОДНОЙ высоте ({self.altitude} м)"

    def __str__(self) -> str:
        return f"Рейс: {self.callsign:<8} | Страна: {self.origin_country:<15} | Скорость: {self.velocity:<5} м/с | Высота: {self.altitude} м"


# --- ФУНКЦИИ БИЗНЕС-ЛОГИКИ (Для удобного тестирования) ---

def filter_by_country(planes: list[Aeroplane], country_name: str) -> list[Aeroplane]:
    """Фильтрация самолетов по стране регистрации (регистронезависимая)"""
    return [p for p in planes if p.origin_country.lower() == country_name.lower().strip()]


def get_top_by_altitude(planes: list[Aeroplane], n: int) -> list[Aeroplane]:
    """Получение топ N самолетов по высоте полета"""
    return sorted(planes, key=lambda p: p.altitude, reverse=True)[:n]


def get_top_by_velocity(planes: list[Aeroplane], n: int) -> list[Aeroplane]:
    """Получение топ N самолетов по скорости полета (использует магические методы)"""
    return sorted(planes, reverse=True)[:n]


# --- ИНТЕРФЕЙС ПОЛЬЗОВАТЕЛЯ ---

def display_table(planes_list: list[Aeroplane], title: str):
    """Красивый вывод таблицы самолетов"""
    width = 60
    header_text = f" {title} "
    print(f"\n{header_text.center(width, '=')}")
    print(f"{'ICAO24':<10} | {'Позывной':<10} | {'Страна':<15} | {'Высота':<8} | {'Скорость':<8}")
    print("-" * width)
    for p in planes_list:
        print(
            f"{p.icao24:<10} | {p.callsign.strip():<10} | {p.origin_country:<15} | {p.altitude:<8.1f} | {p.velocity:<8.1f}")
    print("=" * width)


def run_opensky_menu(planes: list[Aeroplane]):
    """Основной цикл консольного меню"""
    width = 60
    print()
    print(" КОНСОЛЬНЫЙ АНАЛИТИК OPENSKY ".center(width, "="))
    print(f" Доступно самолетов для анализа: {len(planes)} ".center(width, "="))
    print("=" * width)

    while True:
        print("\n--- Меню возможностей ---")
        print("1. Получить самолеты по стране их регистрации")
        print("2. Получить топ N самолетов по высоте полета")
        print("3. Получить топ N самолетов по скорости полета")
        print("4. Сравнить два самолета по высоте")
        print("5. Выйти")

        try:
            choice = input("Выберите действие (1-5): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n[Программа принудительно остановлена пользователем]")
            break

        if choice == "5":
            print("\nЗавершение работы интерфейса.")
            break

        elif choice == "1":
            country = input("Введите название страны (например, 'Germany'): ").strip()
            if not country:
                print("[Ошибка] Название страны не может быть пустым.")
                continue

            filtered = filter_by_country(planes, country)
            if not filtered:
                print(f"Самолетов для страны '{country}' не найдено.")
                continue

            display_table(filtered[:20], f"Самолеты: {country}")

        elif choice in ("2", "3"):
            n_input = input("Введите число N (количество самолетов в топе): ").strip()
            if not n_input.isdigit() or int(n_input) <= 0:
                print("[Ошибка] Введите корректное положительное число.")
                continue

            n = int(n_input)

            if choice == "2":
                top = get_top_by_altitude(planes, n)
                display_table(top, f"Топ {n} по высоте")
            elif choice == "3":
                top = get_top_by_velocity(planes, n)
                display_table(top, f"Топ {n} по скорости")

        elif choice == "4":
            print("\n--- Режим сравнения двух бортов по высоте ---")
            callsign1 = input("Введите позывной первого самолета: ").strip().upper()
            callsign2 = input("Введите позывной второго самолета: ").strip().upper()

            p1 = next((p for p in planes if p.callsign.strip().upper() == callsign1), None)
            p2 = next((p for p in planes if p.callsign.strip().upper() == callsign2), None)

            if not p1 or not p2:
                if not p1: print(f"[Ошибка] Самолет {callsign1} не найден.")
                if not p2: print(f"[Ошибка] Самолет {callsign2} не найден.")
                continue

            print(f"\n[Результат]: {p1.compare_altitude(p2)}")
        else:
            print("[Ошибка] Неверный пункт меню. Попробуйте еще раз.")


if __name__ == "__main__":
    # Демонстрационный набор данных (имитация чтения из json)
    mock_planes = [
        Aeroplane("4b1813", "AFL2130", "Russian Fed.", 10200, 240.5),
        Aeroplane("3c6625", "DLH2TC", "Germany", 9800, 255.2),
        Aeroplane("a1b2c3", "AAL123", "United States", 11500, 230.0),
        Aeroplane("4b1814", "SU100", "Russian Fed.", 8500, 210.0)
    ]

    try:
        run_opensky_menu(mock_planes)
    except KeyboardInterrupt:
        print("\n\n[Программа принудительно остановлена пользователем]")
