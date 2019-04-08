from collections import namedtuple
from typing import List

from .entity import Entity
from .sentence import Sentence
from .text_container import TextContainer

MessageWithCode = namedtuple('MessageWithCode', ['code', 'message'])


class Document(TextContainer):
    """Original text with digest"""
    def __init__(self, text: str):
        TextContainer.__init__(self, text=text)
        self.keywords: List[Entity] = []
        self.entities: List[Entity] = []
        self.digest: List[Entity] = []
        self.sentences: List[Sentence] = []
        self.warnings: List[MessageWithCode] = []
        self.errors: List[MessageWithCode] = []
        self.logs: List[str] = []
