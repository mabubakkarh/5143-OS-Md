from collections.abc import MutableMapping
from random import randint


class Register:
    """Represents a single `register` with a read and write method
    to change the registers values.
    """

    def __init__(self):
        """Constructor"""
        self.contents = 0

    def write(self, x):
        """Change value of register"""
        self.contents = x

    def read(self):
        """Return value of register"""
        return self.contents

    def __str__(self):
        """Print out instance in readable format"""
        return f"[{self.contents}]"

    def __repr__(self):
        """Same as __str__"""
        return self.__str__()
