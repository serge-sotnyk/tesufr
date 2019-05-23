import pytest

from tesufr import SummarySize, TextProcessParams


def test_TextProcessParams_creation():
    params = TextProcessParams(summary_size=SummarySize.new_relative(0.1), keywords_number=0)
    params = TextProcessParams(summary_size=SummarySize.new_relative(0.1), keywords_number=10)


def test_TextProcessParams_keywords_negative():
    with pytest.raises(ValueError):
        TextProcessParams(summary_size=SummarySize.new_relative(0.1), keywords_number=-1)


def test_TextProcessParams_str():
    params = TextProcessParams(summary_size=SummarySize.new_relative(0.1), keywords_number=0)
    s = str(params)
    assert s != ''
    params = TextProcessParams(summary_size=SummarySize.new_absolute(10), keywords_number=0)
    s = str(params)
    assert s != ''
