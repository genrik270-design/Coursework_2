from abc import ABC, abstractmethod
from requests import get

# Создаем абстрактный класс
class BaseAPIAdapter(ABC):

    @abstractmethod
    def get_country_coordinates(self, country: str) -> list:
        """АМ для получения координат страны"""
        pass

    @abstractmethod
    def get_aeroplanes(self, country: str) -> None:
        """АМ для получения данных о самолетах"""
        pass

# Класс наследуемый от абстрактного

class APIAdapter(BaseAPIAdapter):
    def __init__(self) -> None:
        self.openstreetmap_url = "https://openstreetmap.org"
        self.opensky_url = "https://opensky_network.org"
        self.aeroplanes = None

    def get_country_coordinates (self, country: str) -> list:
        """Подключаемся к API Nominatim и получаем координаты страны"""
        headers_nominatim = {
            "User-Agent": "coursework-aviation-app/1.0",
        }
        params_nominatim = {
            "country": country,
            "format": "json",
            "limit": 1,
        }

        response = get(url=self.openstreetmap_url, params=params_nominatim, headers=headers_nominatim)
        data = response.json()

        if not data:
            print(f"Страна '{country}' в базе не найдена")
            return []

        # Возвращаем координаты
        return data [0].get("boundingbox")

    def get_aeroplanes(self, country: str) -> None:
        """Подключается к API OpenSky по данным координатам"""
        geo_coordinates = self.get_country_coordinates(country)
        if not geo_coordinates:
            return
        # Преобразуем строки координат в числа
        params = {
            "lamin": float (geo_coordinates [0]),
            "lamax": float (geo_coordinates [1]),
            "lomin": float (geo_coordinates [2]),
            "lomax": float (geo_coordinates [3]),
        }
        response = get(url=self.opensky_url, params=params)

        if response.status_code != 200:
            print(f"Ошибка OpenSky API: {response.status_code}")
            return

        self.aeroplanes = response.json()
        states = self.aeroplanes.get("states")

        # Выводим результат
        if not states:
            print(f"В воздушном пространстве страны {country} нет самолетов.")
        else:
            print (f"Найдено самолетов над страной {country}: {len(states)}\n")
            print(f"{'Позывной': < 10} | {'Страна регистрации': <20} | {'Высота (м)': <10 } / {'Скорость (м/с)': <15}")
            print("-" * 65)

            for flight in states[:10]:  # Выводим первые 10 самолетов для теста
                callsign = flight[1].strip() if flight[1] else "Н/Д"
                origin_country = flight[2]
                altitude = flight[7] if flight[7] is not None else "Н/Д"
                velocity = flight[9] if flight[9] is not None else "Н/Д"

                print(f"{callsign:<10} | {origin_country:<20} | {altitude:<10} | {velocity:<15}")

