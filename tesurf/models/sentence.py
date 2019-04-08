from .fragment import Fragment
from .text_container import TextContainer


class Sentence(Fragment):
    def __init__(self, owner: TextContainer, start: int, finish: int, lang=""):
        Fragment.__init__(self, owner, start, finish)
        self.lang: str = lang
        self.importance: float = 0.0

    def __repr__(self):
        return f"Sentence({self.owner}, {self.start}, {self.finish}, lang='{self.lang}')"
