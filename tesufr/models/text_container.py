from .text_source import TextSource


class TextContainer(TextSource):
    def __init__(self, text: str):
        self.__text = text

    @property
    def text(self) -> str:
        return self.__text
