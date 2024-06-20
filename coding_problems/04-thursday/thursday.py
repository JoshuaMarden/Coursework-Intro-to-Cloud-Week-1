def pyramid(n: int) -> list:

    filled_array = []
    counter = 0

    for _ in range(n):
        counter += 1
        list_to_insert = [1 for _ in range(counter)]
        filled_array.append(list_to_insert)
        print(list_to_insert)

    return filled_array


if __name__ == "__main__":
    # print(pyramid(0))
    # print(pyramid(1))
    # print(pyramid(2))
    print(pyramid(3))
