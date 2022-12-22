from iterator_class import Iterator


def main():
    i = Iterator("annotation.csv", "rose")
    for val in i:
        print(val)

    print('program _2_get_way_from_csv finished')


if __name__ == '__main__':
    main()
