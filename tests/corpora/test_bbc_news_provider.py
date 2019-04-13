from itertools import zip_longest

from tesurf.corpora import CorpusPurpose, SetType
from tesurf.corpora.providers import BbcNewsProvider


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


def test_bbc_news_provider_sentences_divider():
    text = """TimeWarner said fourth quarter sales rose 2% to $11.1bn from $10.9bn.For the full-year, TimeWarner posted a profit of $3.36bn, up 27% from its 2003 performance, while revenues grew 6.4% to $42.09bn.Quarterly profits at US media giant TimeWarner jumped 76% to $1.13bn (Â£600m) for the three months to December, from $639m year-earlier.However, the company said AOL's underlying profit before exceptional items rose 8% on the back of stronger internet advertising revenues.Its profits were buoyed by one-off gains which offset a profit dip at Warner Bros, and less users for AOL.For 2005, TimeWarner is projecting operating earnings growth of around 5%, and also expects higher revenue and wider profit margins.It lost 464,000 subscribers in the fourth quarter profits were lower than in the preceding three quarters.Time Warner's fourth quarter profits were slightly better than analysts' expectations."""
    sents = list(BbcNewsProvider._bbc_sentences_divider(text))
    assert len(sents) == 8

    text = '''"It looks pretty grim," said Swedish trades union official Ulf Carlsson. "What are we going to end up producing in Sweden?"'''
    sents = list(BbcNewsProvider._bbc_sentences_divider(text))
    assert len(sents) == 2

    text = '''The physical demands of the day-to-day grind will only get harder for Holmes, who has already admitted she "doesn't like the training anymore."So, why is Holmes dragging her heels about making a decision on where, when or whether to even bother competing again?Holmes has now pulled out of this weekend's European Indoor Championships, where she was selected for both the 800m and 1500m, because of a hamstring injury.'''
    sents = list(BbcNewsProvider._bbc_sentences_divider(text))
    assert len(sents) == 3
