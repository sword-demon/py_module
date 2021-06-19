def func1():
    yield 1
    yield from func2
    yield 2


def func2():
    yield 3
    yield from func1
    yield 4

