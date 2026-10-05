from aeroplane import Aeroplane


def filter_by_country(planes: list[Aeroplane], country_name: str) -> list[Aeroplane]:
    """Фильтрация самолетов по стране регистрации"""
    return [p for p in planes if p.origin_country.lower() == country_name.lower().strip()]


def get_top_by_altitude(planes: list[Aeroplane], n: int) -> list[Aeroplane]:
    """Получение топ N самолетов по высоте полета"""
    return sorted(planes, key=lambda p: p.altitude, reverse=True)[:n]


def get_top_by_velocity(planes: list[Aeroplane], n: int) -> list[Aeroplane]:
    """Получение топ N самолетов по скорости полета (использует магические методы)"""
    return sorted(planes, reverse=True)[:n]


if __name__ == "__main__":
    from console_ui import run_opensky_menu
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
