import csv


class Iterator:
    def __init__(self, file_name, class_name):
        self.limit = -1
        self.counter = -1
        self.file_name = file_name
        self.class_name = class_name
        self.rows = []
        with open(file_name, encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=";")
            for row in reader:
                if row[2] == class_name:
                    self.rows.append(row[0] + ';' + row[2])
                    self.limit += 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter < self.limit:
            self.counter += 1
            return self.rows[self.counter]
        else:
            print('None')
            raise StopIteration
