import attr
import math
import numpy as np

from copy         import deepcopy
from typing       import Any, Dict, Optional, Iterable, Iterator, Sized
from numbers      import Integral
from numpy.random import RandomState

@attr.s
class ChunkedRange:
    n:          int                   = attr.ib(validator=lambda i, a, x: x >= 1) # type: ignore
    chunk_size: int                   = attr.ib(default=2 ** 20, validator=lambda i, a, x: x >= 1)
    chunks:     Dict[int, np.ndarray] = attr.ib(init=False, factory=dict)

    def __len__(self) -> int:
        return self.n

    def _get_chunk(self, chunk_index: int) -> np.ndarray:
        chunk: Optional[np.ndarray] = self.chunks.get(chunk_index)

        if chunk is None:
            chunk = np.arange(self.chunk_size * chunk_index, min(self.chunk_size * (chunk_index + 1), self.n),
                dtype=np.uint64)
            self.chunks[chunk_index] = chunk

        return chunk

    def __getitem__(self, i: int) -> np.uint64:
        if not (0 <= i < self.n):
            raise IndexError()

        chunk_index = i // self.chunk_size
        return self._get_chunk(chunk_index)[i - self.chunk_size * chunk_index]

    def __setitem__(self, i: int, x: Integral) -> None:
        if not (0 <= i < self.n):
            raise IndexError()

        chunk_index = i // self.chunk_size
        self._get_chunk(chunk_index)[i - self.chunk_size * chunk_index] = x

@attr.s
class Permutation(Sized, Iterable[np.uint64]):
    n:  int         = attr.ib(validator=lambda i, a, x: x >= 1) # type: ignore
    rs: RandomState = attr.ib(factory=np.random.RandomState)
    i:  int         = attr.ib(init=False, default=0)

    def __attrs_post_init__(self) -> None:
        self.init_random_state = deepcopy(self.rs.get_state())
        self.perm = ChunkedRange(self.n)

    def __len__(self) -> int:
        return self.n

    def __iter__(self) -> Iterator[np.uint64]:
        return self

    def __next__(self) -> np.uint64:
        if self.i >= self.n:
            raise StopIteration()

        j = self.rs.randint(self.i, self.n)
        self.perm[self.i], self.perm[j], self.i = self.perm[j], self.perm[self.i], self.i + 1
        return self.perm[self.i - 1]

    def __getstate__(self) -> Dict[str, Any]:
        return {'n': self.n, 'init_random_state': self.init_random_state, 'i': self.i}

    def __setstate__(self, state: Dict[str, Any]) -> None:
        self.n, self.i = state['n'], 0
        self.rs = RandomState()
        self.rs.set_state(state['init_random_state'])
        self.__attrs_post_init__()

        for _ in range(state['i']):
            next(self)
