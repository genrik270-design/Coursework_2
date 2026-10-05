# api.py
from abc import ABC, abstractmethod
from requests import get
from aeroplane import Aeroplane  # <-- Импортируем класс самолета!


# Создаем абстрактный класс
class BaseAPIAdapter(ABC):

    @abstractmethod
    def get_country_coordinates(self, country: str) -> list:
        """АМ для получения координат страны"""
        pass

    @abstractmethod
    def get_aeroplanes(self, country: str) -> list[Aeroplane]:
        """АМ для получения данных о самолетах"""
        pass


# Класс наследуемый от абстрактного
class APIAdapter(BaseAPIAdapter):
    def __init__(self) -> None:
        # Указываем URL OpenStreetMap и OpenSky Network
        self.openstreetmap_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all"
        self.aeroplanes = None

    def get_country_coordinates(self, country: str) -> list:
        """Подключаемся к API Nominatim и получаем координаты страны"""
        headers_nominatim = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
,
        }
        params_nominatim = {
            "country": country,
            "format": "json",
            "limit": 1,
        }

        try:
            response = get(url=self.openstreetmap_url, params=params_nominatim, headers=headers_nominatim)
            data = response.json()
        except Exception as e:
            print(f"[Ошибка сети Nominatim]: {e}")
            return []

        if not data:
            print(f"Страна '{country}' в географической базе Nominatim не найдена.")
            return []

        # Возвращаем координаты boundingbox
        return data[0].get("boundingbox")

    def get_aeroplanes(self, country: str) -> list[Aeroplane]:
        """Подключается к API OpenSky по данным координатам и возвращает список объектов Aeroplane"""
        geo_coordinates = self.get_country_coordinates(country)
        if not geo_coordinates:
            return []

        # Преобразуем строки координат в числа
        params = {
            "lamin": float(geo_coordinates[0]),
            "lamax": float(geo_coordinates[1]),
            "lomin": float(geo_coordinates[2]),
            "lomax": float(geo_coordinates[3]),
        }

        try:
            response = get(url=self.opensky_url, params=params)
        except Exception as e:
            print(f"[Ошибка сети OpenSky]: {e}")
            return []

        if response.status_code != 200:
            print(f"Ошибка OpenSky API: {response.status_code}")
            return []

        self.aeroplanes = response.json()
        states = self.aeroplanes.get("states")

        if not states:
            print(f"В воздушном пространстве страны {country} сейчас нет активных самолетов.")
            return []

        # Создаем список ООП-объектов Aeroplane
        aeroplanes_objects = []
        for flight in states:
            # Защита по высоте: проверяем None и отсекаем отрицательные числа
            raw_alt = flight[7] if flight[7] is not None else 0.0
            safe_altitude = float(raw_alt) if float(raw_alt) >= 0 else 0.0

            # Защита по скорости: проверяем None и отсекаем отрицательные числа
            raw_vel = flight[9] if flight[9] is not None else 0.0
            safe_velocity = float(raw_vel) if float(raw_vel) >= 0 else 0.0

            plane_object = Aeroplane(
                icao24=flight[0],
                callsign=flight[1].strip() if flight[1] else "Н/Д",
                origin_country=flight[2],
                altitude=safe_altitude,
                velocity=safe_velocity
            )
            aeroplanes_objects.append(plane_object)
        aeroplanes_objects.append(plane_object)

        return aeroplanes_objects
