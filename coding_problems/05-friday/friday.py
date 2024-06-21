def is_valid_IP(strng: str) -> bool:

    for char in strng:
        if not char in ["1", '2', '3', '4', '5', '6', '7', '8', '9', '0', '.']:
            return False

    fragments = strng.split(".")

    if not len(fragments) == 4:
        return False

    for octet in fragments:
        if octet == "":
            return False
        if not 0 <= int(octet) < 256:
            return False
        if octet[0] == '0' and len(octet) > 1:
            return False

    return True


if __name__ == "__main__":

    # print(is_valid_IP('1.2.3.4'))
    # print(is_valid_IP('123.45.67.89'))

    # print(is_valid_IP('1.2.3'))
    # print(is_valid_IP('123.456.78.90'))
    print(is_valid_IP('127.1.1.0'))
