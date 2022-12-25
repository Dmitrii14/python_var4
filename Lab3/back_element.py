import csv


def back_element(filename: str, class_name: str):
    """
        данная функция получает имя файла и класс и возращает предыдущий элемент
    """
    with open(filename, 'r', newline='') as file:
        wr = csv.reader(file, delimiter=' ', quotechar='|')
        i = 0
        saver = 0
        num_list = []
        num = ''
        for char in class_name:
            if char.isdigit():
                num = num + char
            else:
                if num != '':
                    num_list.append(int(num))
                    num = ''
        if num != '':
            num_list.append(int(num))
        for row in wr:
            if i != 0:
                exist = class_name in row[0]
                if exist:
                    res = row[0].split(";")[1].replace("\\", "/")
                    return res.replace(str(num_list[0]), str(num_list[0]-1))
            i += 1
    return None


def next_element(filename: str, class_name: str):
    """
        данная функция получает имя файла и класс и возращает следующий элемент
    """
    with open(filename, 'r', newline='') as file:
        wr = csv.reader(file, delimiter=' ', quotechar='|')
        i = 0
        status = False
        for row in wr:
            if i != 0:
                exist = class_name in row[0]
                if status:
                    return str(row[0].split(";")[1])
                if exist:
                    status = True
            i += 1
    return None


if __name__ == "__main__":
    next = next_element("annotation.csv", "dataset\\rose\\0004.jpg")
    back = back_element("annotation.csv", "dataset\\rose\\0004.jpg")
    print(next, back)
