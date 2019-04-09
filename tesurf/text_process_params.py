from .summary_size import SummarySize


class TextProcessParams:
    """Parameters for processing text by Processor"""

    def __init__(self,
                 summary_size: SummarySize,
                 keywords_number: int = 0):
        self.summary_size = summary_size
        if keywords_number < 0:
            raise ValueError("'keywords_number' should be non-negative value, but '{}' passed".format(keywords_number))
        self.keywords_number = keywords_number
