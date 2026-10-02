from aeroplane import Aeroplane


def run_opensky_menu(planes: list[Aeroplane]):
    print("\n" + "=" * 40)
    print("=== КОНСОЛЬНЫЙ АНАЛИТИК OPENSKY ===")
    print(f"Доступно самолетов для анализа: {len(planes)}")
    print("=" * 40)

    while True:
        print("\n--- Меню возможностей ---")
        print("1. Получить самолеты по стране их регистрации")
        print("2. Получить топ N самолетов по высоте полета")
        print("3. Получить топ N самолетов по скорости полета (Доп. фича через __lt__)")
        print("4. Сравнить два самолета по высоте (Доп. фича через compare_altitude)")
        print("5. Выйти")

        # Выбор
        choice = input("Выберите действие (1-5): ").strip()
        if choice == "5":
            print("\nЗавершение работы интерфейса.")
            break

        elif choice == "1":
            country = input("Введите название страны: ").strip()
            if not country:
                print("[Ошибка] Название страны не может быть пустым.")
                continue

            filtered = [p for p in planes if p.origin_country.lower() == country.lower()]

            if not filtered:
                print(f"Самолетов для страны '{country}' не найдено.")
                continue

            print(f"\nНайдено самолетов страны {country}: {len(filtered)}")
            _display_table(filtered[:20], f"Самолеты зарегистрированные в {country} (Топ-20)")

        elif choice in ("2", "3"):
            n_input = input("Введите число N (количество самолетов в топе): ").strip()
            if not n_input.isdigit() or int(n_input) <= 0:
                print("[Ошибка] Введите корректное положительное число.")
                continue

            n = int(n_input)

            if choice == "2":
                # Сортировка по высоте
                top_planes = sorted(planes, key=lambda p: p.altitude, reverse=True)[:n]
                _display_table(top_planes, f"Топ {n} самолетов по ВЫСОТЕ полета")

            elif choice == "3":
                # Сортировка по скорости (автоматически использует ваши методы __lt__ / __gt__)
                top_planes = sorted(planes, reverse=True)[:n]
                _display_table(top_planes, f"Топ {n} самолетов по СКОРОСТИ полета")

        elif choice == "4":
            print("\n--- Режим сравнения двух бортов по высоте ---")
            callsign1 = input("Введите позывной первого самолета: ").strip().upper()
            callsign2 = input("Введите позывной второго самолета: ").strip().upper()

            p1 = next((p for p in planes if p.callsign.strip().upper() == callsign1), None)
            p2 = next((p for p in planes if p.callsign.strip().upper() == callsign2), None)

            if not p1 or not p2:
                if not p1: print(f"[Ошибка] Самолет {callsign1} не найден в текущей базе.")
                if not p2: print(f"[Ошибка] Самолет {callsign2} не найден в текущей базе.")
                continue

            print("\n[Результат сравнения]:")
            print(p1.compare_altitude(p2))

        else:
            print("[Ошибка] Неверный пункт меню. Попробуйте еще раз.")


def _display_table(planes_list: list[Aeroplane], title: str):
    """Внутренняя вспомогательная функция для красивой отрисовки таблицы"""
    print(f"\n{'=' * 25} {title} {'=' * 25}")
    print(
        f"{'ICAO24':<10} | {'Позывной':<10} | {'Страна регистрации':<20} | {'Высота (м)':<12} | {'Скорость (м/с)':<14}")
    print("-" * 75)
    for p in planes_list:
        print(
            f"{p.icao24:<10} | {p.callsign.strip():<10} | {p.origin_country:<20} | {p.altitude:<12.1f} | {p.velocity:<14.1f}")
    print("=" * (52 + len(title)))
