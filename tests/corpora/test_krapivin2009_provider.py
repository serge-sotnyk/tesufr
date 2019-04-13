from itertools import zip_longest

from tesufr.corpora import CorpusPurpose, SetType
from tesufr.corpora.providers import Krapivin2009Provider


def test_krapivin2009_provider_initialization():
    bbc_news_provider = Krapivin2009Provider()
    assert bbc_news_provider is not None


def test_krapivin2009_provider_metainfo():
    bbc_news_provider = Krapivin2009Provider()
    assert bbc_news_provider.language() == 'en'
    assert bbc_news_provider.purpose() == CorpusPurpose.SUMMARY|CorpusPurpose.KEYWORDS


def test_krapivin2009_provider_extract_subset():
    bbc_news_provider = Krapivin2009Provider()
    for s in [SetType.ALL, SetType.TRAINING, SetType.DEV, SetType.TEST]:
        assert len(list(bbc_news_provider.subset(s))) > 10


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

