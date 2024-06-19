def diamond(n: int) -> str:

    if n == 1:
        return ("*\n")

    # 1,5,13
    manipulated_int = n

    while int(manipulated_int) > 1:
        manipulated_int = (manipulated_int-3)/2

    if manipulated_int == 1:
        half_diamond = n/2

        return_list = []
        stars_to_add = -1
        stars_added = 0

        while stars_added < half_diamond:
            stars_to_add += 2
            for _ in range(stars_to_add):
                return_list.append("*")
                stars_added += 1
            return_list.append("\n")

        while stars_to_add >= 1:
            stars_to_add -= 2
            for _ in range(stars_to_add):
                return_list.append("*")
            return_list.append("\n")

        return_string = "".join(return_list)

        return return_string

    else:

        return None


if __name__ == "__main__":
    print(diamond(5))
    print(diamond(13))
    print(diamond(8))
