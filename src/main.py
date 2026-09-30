import json
import re
from aeroplane import Aeroplane
from connector import JSONConnector
from console_ui import run_opensky_menu


def load_and_parse_task_file(file_path: str):
    print(f"--- Чтение и очистка файла задания: {file_path} ---")

    try:
        # Читаем файл как обычный текстовый документ
        with open(file_path, "r", encoding="utf-8") as file:
            raw_content = file.read()

        # Удаляем все комментарии вида // ...до конца строки и все запятые перед скобками
        clean_content = re.sub(re.compile(r"//.*?\n"), "\n", raw_content)

        # Парси м очищенный от // текст в стандартный словарь Python
        data = json.loads(clean_content)
        states = data.get("states", [])

        print(f"Найдено самолетов в файле: {len(states)}\n")

        # Список для хранения созданных ООП-объектов
        aeroplanes_objects = []

        # Проходим по массиву и создаем объекты класса Aeroplane
        for flight in states:
            plane_object = Aeroplane(
                icao24=flight[0],
                callsign=flight[1],
                origin_country=flight[2],
                altitude=flight[7],  # bar_altitude из вашего файла
                velocity=flight[9]  # velocity из вашего файла
            )
            aeroplanes_objects.append(plane_object)

        return aeroplanes_objects

    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")
        return []


if __name__ == "__main__":
    import os

    # Автоматически определяет папку, где лежит сам файл main.py (то есть src)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Находит файл в корневой папке относительно папки src
    task_file = os.path.join(current_dir, "../opensky-network.response.json")

    # Инициализируем коннектор базы данных
    db = JSONConnector(os.path.join(current_dir, "../database.json"))

    # Чтение -> очистка от // -> создание объектов из исходного файла
    planes = load_and_parse_task_file(task_file)

    # Если в файле задания что-то нашлось, сначала сохраняем это в базу
    if planes:
        print("--- 1. Сохранение новых объектов в базу данных JSON ---")
        for plane in planes:
            db.add_aeroplane(plane)

    # ВЫГРУЖАЕМ ВООБЩЕ ВСЕ САМОЛЕТЫ, КОТОРЫЕ НАКОПИЛИСЬ В БАЗЕ ДАННЫХ
    all_planes_from_db = db.get_aeroplanes_by_criteria({})
    print(f"\n[Успешно загружено из базы данных для меню: {len(all_planes_from_db)} самолетов]")

    try:
        # Запускаем интерактивное меню со ВСЕМИ накопленными самолетами
        run_opensky_menu(all_planes_from_db)
    except KeyboardInterrupt:
        print("\n\n[Программа принудительно остановлена пользователем]")

    # --- Этот отладочный блок выполнится ТОЛЬКО ПОСЛЕ того, как вы выберете пункт "Выйти" в меню ---
    print("\n--- 2. Поиск в базе данных по критерию (Страна: Switzerland) ---")
    search_criteria = {"origin_country": "Switzerland"}
    found_planes = db.get_aeroplanes_by_criteria(search_criteria)

    for p in found_planes:
        print(f"Найдено в базе -> {p}")

    print("\n--- 3. Удаление отладочного объекта из базы по критерию (Позывной: SWR438A) ---")
    delete_criteria = {"callsign": "SWR438A"}
    db.delete_aeroplanes(delete_criteria)

    # Проверяем базу после удаления
    print(f"Осталось самолетов в Швейцарии: {len(db.get_aeroplanes_by_criteria(search_criteria))}")
