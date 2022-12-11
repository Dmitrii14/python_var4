import csv
from main import Data


def next_element(obj: type(Data), pointer: str) -> str:

    with open('annotation.csv', 'r', newline='') as file:
        wr = csv.reader(file, delimiter=' ', quotechar='|')
        i = 0
        status = False
        for row in wr:
            if i != 0:
                exist = pointer in row[1]
                if status:
                    return "next--> " + str(row[1].split(",")[1])
                if exist:
                    status = True
            i += 1
    return None


if __name__ == "__main__":
    obj = Data("dataset")
    next = next_element(obj, "dataset\\rose\\0751.jpg")
    print(next)
