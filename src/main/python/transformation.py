if __name__ == '__main__':
    file_name = "../../resources/transformation_enc"
    with open(file_name, 'r') as f:
        enc = f.read()

    flag = ''
    for token in enc:
        first = ord(token) // (1 << 8)
        second = ord(token) % (1 << 8)
        flag += chr(first) + chr(second)
    print(flag)
