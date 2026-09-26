import io
import os
import sys
import unittest
from unittest.mock import patch

# Добавляем пути к папке src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Импортируем только то, что реально есть в ваших файлах
from src.aeroplane import Aeroplane
from src.console_ui import run_opensky_menu


class TestAeroplaneClass(unittest.TestCase):
    """Тестирование валидации и встроенных методов класса Aeroplane"""

    def test_valid_creation(self):
        plane = Aeroplane("4b1813", "AFL2130 ", "Germany", 10000, 250)
        self.assertEqual(plane.icao24, "4b1813")
        self.assertEqual(plane.callsign, "AFL2130 ")
        self.assertEqual(plane.altitude, 10000.0)

    def test_invalid_altitude_string(self):
        with self.assertRaises(ValueError):
            Aeroplane("4b1813", "AFL", "Germany", "высоко", 250)

    def test_invalid_velocity_negative(self):
        with self.assertRaises(ValueError):
            Aeroplane("4b1813", "AFL", "Germany", 1000, -50)

    def test_none_values_handling(self):
        # Если пришли None, сеттеры должны заменить их на 0.0 или дефолтные строки
        plane = Aeroplane("4b1813", "", None, None, None) # noqa
        self.assertEqual(plane.callsign, "Н/Д")
        self.assertEqual(plane.origin_country, "Н/Д")
        self.assertEqual(plane.altitude, 0.0)
        self.assertEqual(plane.velocity, 0.0)

    def test_magic_comparisons_by_velocity(self):
        plane_slow = Aeroplane("1", "A", "Country", 5000, 100.0)
        plane_fast = Aeroplane("2", "B", "Country", 5000, 200.0)

        self.assertTrue(plane_slow < plane_fast)
        self.assertTrue(plane_fast > plane_slow)
        self.assertFalse(plane_slow == plane_fast)

    def test_compare_altitude_method(self):
        p_high = Aeroplane("1", "HIGH", "Country", 12000, 200)
        p_low = Aeroplane("2", "LOW", "Country", 8000, 200)

        result = p_high.compare_altitude(p_low)
        self.assertIn("ВЫШЕ", result)


class TestConsoleMenu(unittest.TestCase):
    """Тестирование сценариев взаимодействия с пользователем в меню console_ui"""

    def setUp(self):
        # Готовим тестовый список из двух самолетов
        self.data = [
            Aeroplane("1a", "AFL123", "Russian Fed.", 10000, 200),
            Aeroplane("2b", "DLH55", "Germany", 9000, 220)
        ]

    @patch('builtins.input', side_effect=['5'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_menu_exit(self, mock_stdout, _mock_input):
        """Проверка чистого выхода из меню (Пункт 5)"""
        run_opensky_menu(self.data)
        self.assertIn("Завершение работы интерфейса.", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['1', 'Germany', '5'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_menu_search_by_country(self, mock_stdout, _mock_input):
        """Проверка поиска по стране через меню (Пункт 1)"""
        run_opensky_menu(self.data)
        output = mock_stdout.getvalue()
        # Проверяем, что в консоль вывелся немецкий самолет
        self.assertIn("DLH55", output)

    @patch('builtins.input', side_effect=['2', '1', '5'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_menu_top_altitude(self, mock_stdout, _mock_input):
        """Проверка вывода топа высоты через меню (Пункт 2)"""
        run_opensky_menu(self.data)
        output = mock_stdout.getvalue()
        # Проверяем, что вывелся самый высокий самолет (AFL123 с 10000м)
        self.assertIn("AFL123", output)

    @patch('builtins.input', side_effect=['4', 'AFL123', 'DLH55', '5'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_menu_compare_altitude(self, mock_stdout, _mock_input):
        """Проверка вызова функции сравнения через меню (Пункт 4)"""
        run_opensky_menu(self.data)
        output = mock_stdout.getvalue()
        # Ищем ключевое слово из метода compare_altitude
        self.assertIn("ВЫШЕ", output)


if __name__ == "__main__":
    unittest.main()
