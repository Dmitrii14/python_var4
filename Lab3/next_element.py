import csv


def next_element(filename, class_name):
    with open(filename, 'r', newline='') as file:
        wr = csv.reader(file, delimiter=' ', quotechar='|')
        i = 0
        status = False
        for row in wr:
            if i != 0:
                exist = class_name in row[0]
                if status:
                    return "next " + str(row[0].split(";")[0])
                if exist:
                    status = True
            i += 1
    return None
