from enum import IntFlag


class CorpusPurpose(IntFlag):
    """
    Defines, what corpus contains - keywords, summary or both.
    """
    KEYWORDS = 1
    SUMMARY = 2
