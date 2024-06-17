def wave(people: str) -> list[str]:

    wave_list = []

    people = list(people)

    for index, char in enumerate(people):
        if char == " ":
            continue

        people[index] = people[index].upper()
        wave_list.append("".join(people))
        people[index] = people[index].lower()

    return wave_list


if __name__ == "__main__":
    print(wave('hello'))
