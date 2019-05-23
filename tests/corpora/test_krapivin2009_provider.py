from itertools import zip_longest

from tesufr.corpora import CorpusPurpose, SetType
from tesufr.corpora.providers import Krapivin2009Provider


def test_krapivin2009_provider_initialization():
    corpus_provider = Krapivin2009Provider()
    assert corpus_provider is not None


def test_krapivin2009_provider_metainfo():
    corpus_provider = Krapivin2009Provider()
    assert corpus_provider.language() == 'en'
    assert corpus_provider.purpose() == CorpusPurpose.SUMMARY|CorpusPurpose.KEYWORDS


def test_krapivin2009_provider_extract_subset():
    corpus_provider = Krapivin2009Provider()
    for s in [SetType.ALL, SetType.TRAINING, SetType.DEV, SetType.TEST]:
        assert len(list(corpus_provider.subset(s))) > 10


def test_krapivin2009_provider_subset_order():
    corpus_provider = Krapivin2009Provider()
    corpus_provider2 = Krapivin2009Provider()
    for s in [SetType.ALL, SetType.TRAINING, SetType.DEV, SetType.TEST]:
        set1 = list(corpus_provider.subset(s))
        set2 = list(corpus_provider2.subset(s))
        for s1, s2 in zip_longest(set1, set2):
            assert s1.id_ == s2.id_
            assert s1.text == s2.text
            assert s1.lang == s2.lang
            assert '\n'.join(s1.ref_summary) == '\n'.join(s2.ref_summary)
            assert '\n'.join(s1.ref_keywords) == '\n'.join(s2.ref_keywords)

