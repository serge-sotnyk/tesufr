from typing import Iterable

from tesufr.corpora import SetType, CorpusDocument, CorpusPurpose
from .. import ProviderBase


class LimitedProvider(ProviderBase):
    """Provider for debug purposes - returns only first records from inner provider."""

    def __init__(self, inner_provider: ProviderBase, max_docs: int = 10):
        self.inner_provider: ProviderBase = inner_provider
        self.max_docs = max_docs

    def purpose(self) -> CorpusPurpose:
        return self.inner_provider.purpose()

    def subset(self, type_of_set: SetType) -> Iterable[CorpusDocument]:
        for doc, i in zip(self.inner_provider.subset(type_of_set), range(self.max_docs)):
            yield doc

    def subset_size(self, type_of_set: SetType) -> int:
        return min(self.max_docs, self.inner_provider.subset_size(type_of_set))
