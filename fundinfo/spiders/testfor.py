def text():
    print("123")
    for x in [0,1,2,3]:
        print(x)
        yield x


if __name__ == '__main__':
    a = text()
    a.__next__()
    a.__next__()
    print("haha")