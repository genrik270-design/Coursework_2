from abc import ABC, abstractmethod
import json
import os
from aeroplane import Aeroplane


# Абстрактный класс-коннектор

class BaseConnector(ABC):

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Метод для добавления информации о самолете"""
        pass

    @abstractmethod
    def get_aeroplanes_by_criteria(self, criteria: dict) -> list:
        """Метод для поиска данных по критериям"""
        pass

    @abstractmethod
    def delete_aeroplanes(self, criteria: dict) -> None:
        """Метод для удаления информации о самолетах"""
        pass


# Конкретная реализация коннектора для работы с JSON-файлом
class JSONConnector(BaseConnector):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        # Если файла еще нет, создаем пустой JSON-массив
        if not os.path.exists(self.file_path):
            self._save_to_file([])

    def _read_file(self) -> list:
        """Внутренний вспомогательный метод для чтения JSON"""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def _save_to_file(self, data: list) -> None:
        """Внутренний вспомогательный метод для записи в JSON"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Превращает объект Aeroplane в словарь и дописывает в JSON-файл"""
        data = self._read_file()

        # Инкапсуляция данных объекта в словарь для сохранения
        plane_dict = {
            "icao24": aeroplane.icao24,
            "callsign": aeroplane.callsign,
            "origin_country": aeroplane.origin_country,
            "altitude": aeroplane.altitude,
            "velocity": aeroplane.velocity
        }

        # Проверяем, нет ли уже самолета с таким ICAO24 в базе
        if not any(p["icao24"] == aeroplane.icao24 for p in data):
            data.append(plane_dict)
            self._save_to_file(data)
            print(f"Самолет {aeroplane.callsign} успешно сохранен в базу JSON.")

    def get_aeroplanes_by_criteria(self, criteria: dict) -> list:
        """
        Ищет самолеты по переданным критериям (например: {'origin_country': 'Germany'})
        Возвращает список готовых объектов Aeroplane
        """
        data = self._read_file()
        results = []

        for item in data:
            match = True
            for key, value in criteria.items():
                if item.get(key) != value:
                    match = False
                    break
            if match:
                # Превращаем сохраненный словарь обратно в полноценный ООП-объект
                results.append(Aeroplane(
                    icao24=item["icao24"],
                    callsign=item["callsign"],
                    origin_country=item["origin_country"],
                    altitude=item["altitude"],
                    velocity=item["velocity"]
                ))
        return results

    def delete_aeroplanes(self, criteria: dict) -> None:
        """Удаляет из файла все самолеты, подходящие под критерии"""
        data = self._read_file()
        # Оставляем только те элементы, которые НЕ подходят под критерии удаления
        new_data = []

        for item in data:
            match = True
            for key, value in criteria.items():
                if item.get(key) != value:
                    match = False
                    break
            if not match:
                new_data.append(item)

        deleted_count = len(data) - len(new_data)
        self._save_to_file(new_data)
        print(f"Из базы JSON удалено записей: {deleted_count}")
