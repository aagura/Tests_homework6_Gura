
class DataManager:
    @staticmethod
    def get_data(source1, source2):
        try:
            if source1 == 'file' and source2 == 'file':
                return (
                    DataManager.read_numbers_from_file('data1.txt'),
                    DataManager.read_numbers_from_file('data2.txt')
                )
            elif source1 == 'api' and source2 == 'api':
                return (
                    DataManager.fetch_numbers_from_api(),
                    DataManager.fetch_numbers_from_api()
                )
            else:
                raise ValueError("Неподдерживаемый источник данных")
        except ValueError as ve:
            print(f"Ошибка при получении данных: {str(ve)}")
            raise
        except Exception as e:
            print(f"Другая ошибка при получении данных: {str(e)}")
            return None, None

    @staticmethod
    def read_numbers_from_file(file_path):
        try:
            with open(file_path, 'r') as file:
                line = file.readline().strip()
                if not line:
                    raise ValueError("Файл пустой")
                numbers = [float(num) for num in line.split()]
            return numbers
        except Exception as e:
            raise ValueError(f"Ошибка при чтении данных из файла '{file_path}': {str(e)}")

    @staticmethod
    def fetch_numbers_from_api():
        return [1, 2, 3, 4, 5]
