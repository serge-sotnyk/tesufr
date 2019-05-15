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

    _land_dic = {
        "ar": "arabic",
        "da": "danish",
        "nl": "dutch",
        "en": "english",
        "fi": "finnish",
        "fr": "french",
        "de": "german",
        "hu": "hungarian",
        "it": "italian",
        "no": "norwegian",
        "pl": "polish",
        "pt": "portuguese",
        "ro": "romanian",
        "ru": "russian",
        "sp": "spanish",
        "sv": "swedish",
    }

    def process_document(self, doc: Document, text_process_params: TextProcessParams):
        doc.keywords.clear()
        doc.entities.clear()

        parse_sentences(doc)
        main_lang = doc.main_lang
        summa_lang = self._land_dic[main_lang]

        # Extract keywords
        text = doc.text
        kw_num = text_process_params.keywords_number
        if kw_num <= 0:
            kw_num = 10
        kwrds = keywords.keywords(text, words=kw_num, language=summa_lang)

        # Extract summary
        ratio = text_process_params.summary_size.calculate_ratio(len(doc.sentences))
        summary = summarizer.summarize(text, ratio=ratio, language=summa_lang)
        # print(kwrds)
        # print(summary)
        for kw in kwrds.splitlines():
            doc.keywords.append(Entity(kw, EntityKind.KEYWORD))
        for s in summary.splitlines():
            doc.summary.append(Entity(s, EntityKind.SUMMARY_SENTENCE))

    def can_process(self, doc: Document, text_process_params: TextProcessParams) -> bool:
        return doc.main_lang in self._land_dic
