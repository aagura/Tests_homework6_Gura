
from calculator import Calculator
from data_manager import DataManager
from comparator import NumberComparator


def main():
    data_source1 = 'file'
    data_source2 = 'file'

    numbers1, numbers2 = DataManager.get_data(data_source1, data_source2)

    if numbers1 is None or numbers2 is None:
        print("Не удалось получить данные. Программа завершена.")
        return

    if not numbers1 or not numbers2:
        print("Один из списков пуст. Невозможно выполнить сравнение.")
        return

    average1 = Calculator(numbers1).calculate_average()
    average2 = Calculator(numbers2).calculate_average()

    result = NumberComparator.compare_averages(average1, average2)
    print(result)
    return (result)


if __name__ == "__main__":
    main()
