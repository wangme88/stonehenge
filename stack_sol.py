""" implement stack ADT
"""
from typing import Any
from typing import List


class Stack:

    """ Last-in, first-out (LIFO) stack.
    """
    _items:List[Any]

    def __init__(self) -> None:
        """ Create a new, empty Stack self.
        @param Stack self: this stack
        @rtype: None
        """
        self._items = []

    def add(self, obj:Any) -> None:
        """ Add object obj to top of Stack self.
        @param Stack self: this Stack
        @param object obj: object to place on Stack
        @rtype: None
        """
        self._items.append(obj)

    def remove(self) -> Any:
        """
        Remove and return top element of Stack self.
        Assume Stack self is not empty.
        @param Stack self: this Stack
        @rtype: object
        >>> s = Stack()
        >>> s.add(5)
        >>> s.add(7)
        >>> s.remove()
        7
        """
        return self._items.pop()

    def is_empty(self) -> bool:
        """
        Return whether Stack self is empty.
        @param Stack self: this Stack
        @rtype: bool
        >>> s = Stack()
        >>> s.add(5)
        >>> s.remove()
        5
        >>> s.is_empty()
        True
        """
        return len(self._items) == 0

    def size(self) -> int:
        """
        Return the size of the stack.
        @param Stack self: this Stack
        @rtype: int

        >>> s = Stack()
        >>> s.add(5)
        >>> s.add(7)
        >>> s.size()
        2
        """
        return len(self._items)


if __name__ == "__main__":
    import doctest
    doctest.testmod()