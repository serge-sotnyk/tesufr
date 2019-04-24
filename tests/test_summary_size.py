import pytest

from tesufr.summary_size import SummarySize


def test_digest_size_relative():
    size = SummarySize.new_relative(relative_part=0.5)
    assert size.calculate_size(100) == 50


def test_digest_size_relative_too_much():
    size = SummarySize.new_relative(3.0)  # 300%
    assert size.calculate_size(100) == 100


def test_digest_size_relative_negative():
    with pytest.raises(ValueError):
        SummarySize.new_relative(-0.1)


def test_digest_size_absolute():
    size = SummarySize.new_absolute(5)
    assert size.calculate_size(100) == 5


def test_digest_size_absolute_too_much():
    size = SummarySize.new_absolute(500000)
    assert size.calculate_size(100) == 100


def test_digest_size_absolute_negative():
    with pytest.raises(ValueError):
        SummarySize.new_absolute(-10)


def test_calculate_ratio_negative():
    with pytest.raises(ValueError):
        SummarySize.new_absolute(3).calculate_ratio(-5)
    with pytest.raises(ValueError):
        SummarySize.new_relative(0.25).calculate_ratio(-200)


def test_calculate_ratio():
    assert SummarySize.new_absolute(5).calculate_ratio(10) == 0.5
    assert SummarySize.new_relative(0.25).calculate_ratio(15) == 0.25
