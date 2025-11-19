# def A():
#     print(1, end=" ")
#     print(2, end=" ")
#     print(3, end=" ")
#
#
# def B():
#     print("x", end=" ")
#     print("y", end=" ")
#     print("z", end=" ")
#
#
# def main():
#     A()
#     B()
#
#
# if __name__ == "__main__":
#     main()


def A():
    print(1, end=" ")
    print(2, end=" ")
    yield
    print(3, end=" ")


def B():
    print("x", end=" ")
    yield
    print("y", end=" ")
    print("z", end=" ")


def run_co(co):
    try:
        next(co)
    except StopIteration:
        pass


def main():
    coA = A()
    coB = B()

    run_co(coA)
    run_co(coB)

    run_co(coA)
    run_co(coB)


if __name__ == "__main__":
    main()
