def meeting(s: str) -> str:
    names = s.upper().split(";")
    split_names = []

    for name in names:
        split_name = name.split(":")
        split_names.append(split_name)

    # Sort by last name first, then by first name
    sorted_names = sorted(split_names, key=lambda name: (name[1], name[0]))

    # Create the formatted string
    formatted_names = ["(" + name[1] + ", " + name[0] +
                       ")" for name in sorted_names]

    return "".join(formatted_names)


if __name__ == "__main__":

    s = "Alexis:Wahl;John:Bell;Victoria:Schwarz;Abba:Dorny;Grace:Meta;Ann:Arno;Madison:STAN;Alex:Cornwell;Lewis:Kern;Megan:Stan;Alex:Korn"
    print(meeting(s))

# (ARNO, ANN)(BELL, JOHN)(CORNWELL, ALEX)(DORNY, ABBA)(KERN, LEWIS)(KORN, ALEX)(META, GRACE)(STAN, MADISON)(SCHWARZ, VICTORIA)(STAN, MEGAN)(WAHL, ALEXIS)
# (ARNO, ANN)(BELL, JOHN)(CORNWELL, ALEX)(DORNY, ABBA)(KERN, LEWIS)(KORN, ALEX)(META, GRACE)(SCHWARZ, VICTORIA)(STAN, MADISON)(STAN, MEGAN)(WAHL, ALEXIS)
