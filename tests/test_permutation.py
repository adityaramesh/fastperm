import time
import pickle
import numpy as np

from fastperm import Permutation

def test_1() -> None:
    s = Permutation(10)
    xs = [i for i in s]
    print(xs)

def test_2() -> None:
    for _ in range(64):
        s = Permutation(10)
        xs = [i for i in s]
        assert sorted(xs) == list(range(10))

def test_3() -> None:
    s = Permutation(10_000_000)
    t0 = time.time()
    xs = [next(s)]
    t1 = time.time() - t0
    xs.extend([i for i in s])
    t2 = time.time() - t0
    assert sorted(xs) == list(range(10_000_000))

    print(f"time to generate first element: {t1} sec")
    print(f"time to generate all elements: {t2} sec")

    t0 = time.time()
    x = np.random.permutation(10_000_000)
    t1 = time.time() - t0

    print(f"time to generate all elements with numpy: {t1} sec")

def test_4() -> None:
    s = Permutation(1_000_000_000)
    print(next(s))

def test_5() -> None:
    s = Permutation(1_000_000)
    [next(s) for _ in range(32)]

    state = pickle.dumps(s)
    xs = [next(s) for _ in range(32)]

    s = pickle.loads(state)
    ys = [next(s) for _ in range(32)]
    assert xs == ys

if __name__ == '__main__':
    #test_1()
    #test_2()
    #test_3()
    #test_4()
    test_5()
