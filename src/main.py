# main.py
import os
from connector import JSONConnector
from console_ui import run_opensky_menu
from app import APIAdapter  # 🎯 Импортируем наш новый класс-адаптер


if __name__ == "__main__":
    # Автоматически определяет папку, где лежит сам файл main.py (то есть src)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Находит файл в корневой папке относительно папки src
    task_file = os.path.join(current_dir, "../opensky-network.response.json")

    # Инициализируем коннектор базы данных
    db = JSONConnector(os.path.join(current_dir, "../database.json"))

    # 🎯 СОЗДАЕМ ЭКЗЕМПЛЯР КЛАССА И ВЫЗЫВАЕМ ЕГО МЕТОД (Чистый ООП стиль)
    adapter = APIAdapter(task_file)
    planes = adapter.load_and_parse()

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
