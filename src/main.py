from requests import get


class APIAdapter:
    def __init__(self) -> None:
        self.openstreetmap_url = 'https://openstreetmap.org'
        # ИСПРАВЛЕНО: Убран знак "?" в конце URL
        self.opensky_url = 'https://opensky-network.org'
        self.aeroplanes = None

    def get_aeroplanes(self, country: str) -> None:
        # Headers c user-agent — обязательный параметр при запросе к nominatim.openstreetmap.
        headers_nominatim = {
            'User-Agent': 'test-app/1.0',
        }

        params_nominatim = {
            'country': country,
            'format': 'json',
            'limit': 1,
        }

        response = get(url=self.openstreetmap_url, params=params_nominatim, headers=headers_nominatim)
        data = response.json()

        # Базовая проверка: нашла ли Nominatim такую страну
        if not data:
            print(f"Страна '{country}' не найдена!")
            return

        geo_coordinates = data[0].get('boundingbox')

        # ИСПРАВЛЕНО: Преобразуем строки координат в числа (float)
        params = {
            'lamin': float(geo_coordinates[0]),
            'lamax': float(geo_coordinates[1]),
            'lomin': float(geo_coordinates[2]),
            'lomax': float(geo_coordinates[3]),
        }

        # Делаем запрос к OpenSky
        response = get(url=self.opensky_url, params=params)

        if response.status_code != 200:
            print(f"Ошибка OpenSky API: {response.status_code}")
            return

        self.aeroplanes = response.json()

        # ДОБАВЛЕНО: Красивый вывод результата в консоль
        states = self.aeroplanes.get("states")
        if not states:
            print(f"В воздушном пространстве страны {country} сейчас нет самолетов.")
        else:
            print(f"Успешно! Найдено самолетов над {country}: {len(states)}\n")
            print(f"{'Позывной':<10} | {'Страна рег.':<15} | {'Высота (м)':<10} | {'Скорость (м/с)':<10}")
            print("-" * 60)
            for flight in states[:10]:  # Выведем первые 10 для теста
                callsign = flight[1].strip() if flight[1] else "N/A"
                origin_country = flight[2]
                altitude = flight[7] if flight[7] is not None else "Н/Д"
                velocity = flight[9] if flight[9] is not None else "Н/Д"
                print(f"{callsign:<10} | {origin_country:<15} | {altitude:<10} | {velocity:<10}")


# Запуск
api = APIAdapter()
api.get_aeroplanes('Canada')
