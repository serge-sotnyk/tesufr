from summa import summarizer, keywords

from .core_utils import parse_sentences
from ..models import Entity, EntityKind
from .. import TextProcessParams
from .core_base import CoreBase
from ..models import Document


class SummaCore(CoreBase):
    """
    Core, based on https://github.com/summanlp/textrank library
    """

    def process_document(self, doc: Document, text_process_params: TextProcessParams):
        doc.keywords.clear()
        doc.entities.clear()

        parse_sentences(doc)

        # Extract keywords
        text = doc.text
        kw_num = text_process_params.keywords_number
        if kw_num <= 0:
            kw_num = 10
        kwrds = keywords.keywords(text, words=kw_num)

        # Extract summary
        ratio = text_process_params.summary_size.calculate_ratio(len(doc.sentences))
        summary = summarizer.summarize(text, ratio=ratio)
        # print(kwrds)
        # print(summary)
        for kw in kwrds.splitlines():
            doc.keywords.append(Entity(kw, EntityKind.KEYWORD))
        for s in summary.splitlines():
            doc.summary.append(Entity(s, EntityKind.SUMMARY_SENTENCE))

    def can_process(self, doc: Document, text_process_params: TextProcessParams) -> bool:
        if doc.main_lang == 'en':
            return True
