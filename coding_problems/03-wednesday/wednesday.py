def meeting(s: str) -> str:

    names = s.split(";")
    split_names = []
    for name in names:
        split_names = name.split(":")
        split_names.append(split_names)

    for i in split_names:
        print(i)

    sorted_names = sorted(split_names, key=lambda name: (name[1], name[0]))
    for index, name in enumerate(sorted_names):
        new_list_element = "(" + (", ".join(names)).upper() + ")"
        sorted_names[index] = new_list_element

    return sorted_names


if __name__ == "__main__":

    s = "Fred:Corwill;Wilfred:Corwill;Barney:Tornbull;Betty:Tornbull;Bjon:Tornbull;Raphael:Corwill;Alfred:Corwill"
    print(meeting(s))
