from itertools import zip_longest

from corpora import CorpusPurpose, SetType
from corpora.providers import BbcNewsProvider


def test_bbc_news_provider_initialization():
    bbc_news_provider = BbcNewsProvider()
    assert bbc_news_provider is not None


def test_bbc_news_provider_metainfo():
    bbc_news_provider = BbcNewsProvider()
    assert bbc_news_provider.language() == 'en'
    assert bbc_news_provider.purpose() == CorpusPurpose.SUMMARY


def test_bbc_news_provider_extract_subset():
    bbc_news_provider = BbcNewsProvider()
    for s in [SetType.ALL, SetType.TRAINING, SetType.DEV, SetType.TEST]:
        assert len(list(bbc_news_provider.subset(s))) > 10


def test_bbc_news_provider_subset_order():
    bbc_news_provider = BbcNewsProvider()
    bbc_news_provider2 = BbcNewsProvider()
    for s in [SetType.ALL, SetType.TRAINING, SetType.DEV, SetType.TEST]:
        set1 = list(bbc_news_provider.subset(s))
        set2 = list(bbc_news_provider2.subset(s))
        for s1, s2 in zip_longest(set1, set2):
            assert s1.id_ == s2.id_
            assert s1.text == s2.text
            assert s1.lang == s2.lang
            assert '\n'.join(s1.ref_summary) == '\n'.join(s2.ref_summary)
            assert '\n'.join(s1.ref_keywords) == '\n'.join(s2.ref_keywords)
