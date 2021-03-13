from fastperm import ChunkedRange

def test_1() -> None:
    r = ChunkedRange(10, chunk_size=20)
    assert len(r) == 10

    print(r[0])
    print(r[9])

    try:
        print(r[10])
    except IndexError:
        pass
    else:
        assert False

def test_2() -> None:
    r = ChunkedRange(10, chunk_size=5)
    assert len(r) == 10

    xs = [r[i] for i in range(10)]
    assert xs == list(range(10))

def test_3() -> None:
    r = ChunkedRange(10, chunk_size=5)

    for i in range(len(r) // 2):
        j = len(r) - i - 1
        r[i], r[j] = r[j], r[i]

    assert [r[i] for i in range(10)] == list(reversed(range(10)))

if __name__ == '__main__':
    #test_1()
    #test_2()
    test_3()
