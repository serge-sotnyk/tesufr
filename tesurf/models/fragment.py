from .text_container import TextContainer
from .text_source import TextSource


class Fragment(TextSource):
    def __init__(self, owner: TextContainer, start: int, finish: int):
        self.__owner = owner
        self.__start = start
        self.__finish = finish

    @property
    def text(self) -> str:
        """Slice text content from owner's text"""
        return self.__owner.text[self.__start:self.__finish]

    @property
    def start(self) -> int:
        """Start position in owner's text."""
        return self.__start

    @property
    def finish(self) -> int:
        """Finish position in owner's text."""
        return self.__finish

    @property
    def owner(self) -> TextContainer:
        """Owner of text"""
        return self.__owner

    def __len__(self):
        return self.__finish - self.__start

    def __str__(self) -> str:
        return self.text

    @staticmethod
    def fragment_with_len(owner: TextContainer, start: int, length: int) -> 'Fragment':
        return Fragment(owner, start, start + length)
