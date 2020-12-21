def root2(n):
    n **= 1/2
    print(n)


def root3(n):
    if n < 0:
        m = -((-n) ** (1/3))
        print(m)
    else:
        n **= 1/3
        print(n)
