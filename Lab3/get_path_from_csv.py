from Lab3.iterator_class import IteratorOfExemplar


if __name__ == '__main__':
    """
        Функция возвращает путь к изображению внутри файла+
    """
    i = IteratorOfExemplar("annotation.csv", "rose")
    for val in i:
        print(val)
    print('program _2_get_way_from_csv finished')
