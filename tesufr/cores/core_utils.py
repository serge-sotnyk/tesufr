from langdetect import DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

from tesufr.models import Sentence
from ..initial_parser import parse_sentences_multilingual
from ..models import Document

_lang_detector_factory = DetectorFactory()


def parse_sentences(doc: Document) -> type(None):
    """Method parses field text in passed document and fills sentences field"""
    raw_sentences = parse_sentences_multilingual(doc.text)
    doc.sentences.clear()
    for sent in raw_sentences:
        sentence = Sentence(doc, sent.start, sent.finish)
        try:
            text = sentence.text
            detector = _lang_detector_factory.create()
            detector.append(text)
            sentence.lang = detector.detect()
        except LangDetectException:
            pass
        doc.sentences.append(sentence)