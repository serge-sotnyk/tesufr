from collections import defaultdict
from typing import List

from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

from tesurf.models import Sentence, Entity, EntityKind
from .core_base import CoreBase
from .. import TextProcessParams
from ..initial_parser import FragmentPositions, parse_paragraphs, parse_sentences_multilingual
from ..models import Document


class FallbackCore(CoreBase):
    """Fallback core"""

    @staticmethod
    def _parse_sentences(doc: Document) -> type(None):
        raw_sentences = parse_sentences_multilingual(doc.text)
        doc.sentences.clear()
        for sent in raw_sentences:
            sentence = Sentence(doc, sent.start, sent.finish)
            try:
                sentence.lang = detect(sentence.text)
            except LangDetectException:
                pass
            doc.sentences.append(sentence)

    def _retrieve_kw(self, doc):
        pass

    def can_process(self, doc: Document, text_process_params: TextProcessParams) -> bool:
        # This core can process any language and params
        return True

    def __init__(self):
        ...

    def process_document(self, doc: Document, text_process_params: TextProcessParams):
        doc.sentences.clear()
        doc.keywords.clear()
        doc.entities.clear()

        self._parse_sentences(doc)
        for i, s in zip(range(text_process_params.summary_size.calculate_size(len(doc.sentences))), doc.sentences):
            summary_sent = Entity(s.text, EntityKind.SUMMARY_SENTENCE)
            summary_sent.entries.append(s)
            doc.summary.append(summary_sent)

        self._retrieve_kw(doc)

        paragraphs: List[FragmentPositions] = parse_paragraphs(doc.text)
        kw_candidates = []
        entities = defaultdict(list)

