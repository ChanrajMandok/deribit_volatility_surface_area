from typing import Dict, Iterator, Mapping, TypeVar

M = TypeVar('M')
E = TypeVar('E')


class StoreInterface(Mapping[E, M]):

    def __init__(self):
        self.d: Dict[E, M] = dict()

    def __getitem__(self, item: E) -> M:
        value = str(item)
        return self.d[value]

    def __len__(self) -> int:
        return len(self.d)

    def __iter__(self) -> Iterator[E]:
        return iter(self.d)
