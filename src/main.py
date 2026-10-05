import os
from connector import JSONConnector
from console_ui import run_opensky_menu
from api import APIAdapter  # Импортируем оригинальный APIAdapter из api.py


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    database_file = os.path.join(current_dir, "../database.json")

    # Инициализируем коннектор базы данных JSON
    db = JSONConnector(database_file)

    print("=== КОНСОЛЬНЫЙ АНАЛИТИК АВИАЦИИ (LIVE API) ===")

    # 1 — Вводим название страны и получаем информацию по API
    country = input("Введите название страны на английском (например, Switzerland, Germany): ").strip()
    if not country:
        print("[Ошибка] Название страны не может быть пустым.")
        return

    # Создаем экземпляр Оригинального класса APIAdapter из модуля api.py
    adapter = APIAdapter()
    print(f"\nВыполняется запрос к API для страны '{country}'...")

    # Получаем список созданных ООП-объектов Aeroplane напрямую из сети
    live_planes = adapter.get_aeroplanes(country)

    # 2 — Сохраняем информацию о полученных самолетах в json файл базы
    if live_planes:
        print(f"Найдено в сети самолетов: {len(live_planes)}. Сохранение в базу database.json...")
        for plane in live_planes:
            db.add_aeroplane(plane)
    else:
        print("[Предупреждение] Из сети не поступило данных для сохранения.")

    # 3 — Считываем информацию с файла и предлагаем Пользователю варианты работы
    print("\nСчитывание актуальных данных из файла базы данных...")
    all_planes_from_db = db.get_aeroplanes_by_criteria({})
    print(f"[Успешно загружено из базы данных для анализа: {len(all_planes_from_db)} самолетов]")

    if not all_planes_from_db:
        print("[Ошибка] В базе данных отсутствуют самолеты для анализа. Меню не может быть запущено.")
        return

    try:
        # Запускаем интерактивное меню со всеми накопленными самолетами из файла базы данных
        run_opensky_menu(all_planes_from_db)
    except KeyboardInterrupt:
        print("\n\n[Программа принудительно остановлена пользователем]")


if __name__ == "__main__":
    main()
