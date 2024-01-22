
class NumberComparator:
    @staticmethod
    def compare_averages(average1, average2):
        if average1 is None and average2 is None:
            return "Средние значения равны"
        elif average1 is None:
            return "Второй список имеет большее среднее значение"
        elif average2 is None:
            return "Первый список имеет большее среднее значение"
        elif float(average1) > float(average2):
            return "Первый список имеет большее среднее значение"
        elif float(average1) < float(average2):
            return "Второй список имеет большее среднее значение"
        else:
            return "Средние значения равны"
