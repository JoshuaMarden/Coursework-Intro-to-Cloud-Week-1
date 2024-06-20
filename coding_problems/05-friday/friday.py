def is_valid_IP(strng: str) -> bool:

    fragments = strng.split(".")

    if not len(fragments) == 4:
        return False

    for octet in fragments:
        if not 0 < int(octet) < 256:
            return False

    return True


if __name__ == "__main__":

    print(is_valid_IP('1.2.3.4'))
    print(is_valid_IP('123.45.67.89'))

    print(is_valid_IP('1.2.3'))
    print(is_valid_IP('123.456.78.90'))
