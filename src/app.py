# app.py
import json
import re
from aeroplane import Aeroplane


class APIAdapter:
    """Класс-адаптер для чтения сырого файла OpenSky и создания ООП-объектов"""
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def load_and_parse(self) -> list[Aeroplane]:
        print(f"--- [APIAdapter] Чтение и очистка файла задания: {self.file_path} ---")
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                raw_content = file.read()

            # Удаляем все комментарии вида // ...до конца строки
            clean_content = re.sub(r"//.*?\n", "\n", raw_content)

            # Парсим очищенный текст в стандартный словарь Python
            data = json.loads(clean_content)
            states = data.get("states", [])

            print(f"Найдено самолетов в файле: {len(states)}\n")

            aeroplanes_objects = []

            # Проходим по массиву и создаем объекты класса Aeroplane
            for flight in states:
                plane_object = Aeroplane(
                    icao24=flight[0],
                    callsign=flight[1],
                    origin_country=flight[2],
                    altitude=flight[7],  # baro_altitude
                    velocity=flight[9]   # velocity
                )
                aeroplanes_objects.append(plane_object)

            return aeroplanes_objects

        except Exception as e:
            print(f"[Ошибка APIAdapter]: {e}")
            return []


# --- ФУНКЦИИ БИЗНЕС-ЛОГИКИ ---

def filter_by_country(planes: list[Aeroplane], country_name: str) -> list[Aeroplane]:
    """Фильтрация самолетов по стране регистрации (регистронезависимая)"""
    return [p for p in planes if p.origin_country.lower() == country_name.lower().strip()]


def get_top_by_altitude(planes: list[Aeroplane], n: int) -> list[Aeroplane]:
    """Получение топ N самолетов по высоте полета"""
    return sorted(planes, key=lambda p: p.altitude, reverse=True)[:n]


def get_top_by_velocity(planes: list[Aeroplane], n: int) -> list[Aeroplane]:
    """Получение топ N самолетов по скорости полета (использует магические методы)"""
    return sorted(planes, reverse=True)[:n]
