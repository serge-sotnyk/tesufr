from enum import IntEnum
from typing import List

from .fragment import Fragment


class EntityKind(IntEnum):
    KEYWORD = 0
    DIGEST_SENTENCE = 1
    NAMED = 2


class Entity:
    def __init__(self, lemma: str, kind: EntityKind, subkind: str = None):
        self._lemma: str = lemma
        self._kind: EntityKind = kind
        self._subkind: str = subkind
        self.entries: List[Fragment] = []

    @property
    def lemma(self):
        return self._lemma

    @property
    def kind(self):
        return self._kind

    @property
    def subkind(self):
        return self._subkind

    def __str__(self):
        return f"{self._kind}:'{self._lemma}'({len(self.entries)})"
