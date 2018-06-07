from collections import deque
from typing import Iterable, Any


class Stack(object):

    def __init__(self, items: Iterable[Any] = None):
        if items is None:
            items = deque()
        else:
            items = deque(items)
        self._items = items

    def peek(self):
        return self._items[-1]

    def pop(self):
        return self._items.pop()

    def push(self, item):
        self._items.append(item)

    def clear(self):
        self._items.clear()

    def __len__(self):
        return len(self._items)

    def __getitem__(self, key):
        return self._items[key]

    def __iter__(self):
        for i in self._items:
            yield i
