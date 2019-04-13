from typing import List


class CorpusDocument:
    """
    Container for information retrieved from corpus about single document.
    """

    def __init__(self,
                 id_: str,
                 text: str = None,
                 ref_keywords: List[str] = None,
                 ref_summary: List[str] = None,
                 lang: str = "en"
                 ):
        """
        Constructor
        :param id_: unique id for document - it should contains information to proper identification
                where it placed in the corpora.
        :param text: full article text
        :param ref_keywords: referenced ("ideal", manually created) keywords
        :param ref_summary: sentences of manually created summary
        :param lang: document language - some languages demand additional language-depended processing
        """
        self.id_ = id_
        self.text = '' if text is None else text
        self.ref_keywords = [] if ref_keywords is None else ref_keywords
        self.ref_summary = [] if ref_summary is None else ref_summary
        self.lang = lang
