from .digest_size import DigestSize


class TextProcessParams:
    """Parameters for processing text by DigestProcessor"""

    def __init__(self,
                 digest_size: DigestSize,
                 keywords_number: int = 0):
        self.digest_size = digest_size
        if keywords_number < 0:
            raise ValueError("'keywords_number' should be non-negative value, but '{}' passed".format(keywords_number))
        self.keywords_number = keywords_number
