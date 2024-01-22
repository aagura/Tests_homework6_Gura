import math
from unittest.mock import mock_open, patch
from data_manager import DataManager
from calculator import Calculator
from comparator import NumberComparator
import pytest

from main import main

main_result = "Средние значения равны"
check_get = 'data_manager.DataManager.get_data'
@pytest.fixture
def file_path():
    file_path = "test_data.txt"
    with open(file_path, 'w') as file:
        file.write("1 2 3 4 5")
    return file_path


def test_read_numbers_from_file(file_path):
    numbers = DataManager.read_numbers_from_file(file_path)
    assert numbers == [1, 2, 3, 4, 5]


def test_read_numbers_from_empty_file(tmp_path):
    empty_file_path = tmp_path / "empty_data.txt"
    with open(empty_file_path, 'w'):
        #Сценарий открытия пустого файоа не требует действий
        pass
    with pytest.raises(ValueError, match="Файл пустой"):
        DataManager.read_numbers_from_file(empty_file_path)


def test_read_numbers_from_nonexistent_file():
    with pytest.raises(ValueError, match="Ошибка при чтении данных из файла"):
        DataManager.read_numbers_from_file("nonexistent_file.txt")


def test_fetch_numbers_from_api():
    numbers = DataManager.fetch_numbers_from_api()
    assert numbers == [1, 2, 3, 4, 5]


def test_get_data_file_file():
    fake_data = "1 2 3 4 5"

    with patch('builtins.open', mock_open(read_data=fake_data)):
        numbers1, numbers2 = DataManager.get_data('file', 'file')

    assert numbers1 == [1, 2, 3, 4, 5]
    assert numbers2 == [1, 2, 3, 4, 5]


def test_get_data_with_api(mocker):
    mocker.patch('data_manager.DataManager.fetch_numbers_from_api', return_value=[1, 2, 3, 4, 5])

    result = DataManager.get_data('api', 'api')

    assert DataManager.fetch_numbers_from_api.call_count == 2

    assert result[0] == [1, 2, 3, 4, 5]
    assert result[1] == [1, 2, 3, 4, 5]


def test_get_data_invalid_source():
    with pytest.raises(ValueError, match="Неподдерживаемый источник данных"):
        DataManager.get_data('invalid', 'invalid')


def test_get_data_exception(mocker):
    mocker.patch('data_manager.DataManager.read_numbers_from_file', side_effect=Exception("File error"))
    numbers1, numbers2 = DataManager.get_data('file', 'file')
    assert numbers1 is None
    assert numbers2 is None


def test_main_integration(mocker, capsys):
    mocker.patch(check_get, return_value=([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]))

    result = main()

    DataManager.get_data.assert_called_once_with('file', 'file')

    expected_result = main_result
    assert result == expected_result

    captured = capsys.readouterr()
    assert main_result in captured.out


def test_calculate_average_with_empty_list():
    calculator = Calculator([])
    assert calculator.calculate_average() == 0


def test_calculate_average_with_non_empty_list():
    calculator = Calculator([1, 2, 3, 4, 5])
    assert math.isclose(calculator.calculate_average(), 3.0)


def test_calculate_average_with_negative_numbers():
    calculator = Calculator([-1, -2, -3, -4, -5])
    assert math.isclose(calculator.calculate_average(), -3.0)


def test_calculate_average_with_none():
    calculator = Calculator(None)
    assert calculator.calculate_average() == 0


def test_compare_averages_first_greater():
    result = NumberComparator.compare_averages(3.0, 2.5)
    assert result == "Первый список имеет большее среднее значение"


def test_compare_averages_second_greater():
    result = NumberComparator.compare_averages(2.5, 3.0)
    assert result == "Второй список имеет большее среднее значение"


def test_compare_averages_equal():
    result = NumberComparator.compare_averages(3.0, 3.0)
    assert result == main_result


def test_compare_averages_first_none():
    result = NumberComparator.compare_averages(None, 3.0)
    assert result == "Второй список имеет большее среднее значение"


def test_compare_averages_second_none():
    result = NumberComparator.compare_averages(3.0, None)
    assert result == "Первый список имеет большее среднее значение"


def test_compare_averages_both_none():
    result = NumberComparator.compare_averages(None, None)
    assert result == main_result


def test_main_data_unavailable(capsys, mocker):
    mocker.patch(check_get, return_value=(None, None))

    main()

    captured = capsys.readouterr()
    assert "Не удалось получить данные. Программа завершена." in captured.out


def test_main_empty_lists(capsys, mocker):
    mocker.patch(check_get, return_value=([], []))

    main()

    captured = capsys.readouterr()
    assert "Один из списков пуст. Невозможно выполнить сравнение." in captured.out
