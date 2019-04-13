from typing import List, Optional

# from .lang_cores import can_process_lang, construct_spacy_core, CoreBase
from langdetect import detect, detect_langs
from langdetect.lang_detect_exception import LangDetectException
from langdetect.language import Language

from .cores import FallbackCore
from .cores import CoreBase
from .initial_parser import parse_sentences_multilingual
from .models import Document, Sentence, MessageWithCode
from .text_process_params import TextProcessParams

"""
def parse_sentences(document: Document) -> type(None):
    raw_sentences = parse_sentences_multilingual(document.text)
    document.sentences.clear()
    for sent in raw_sentences:
        sentence = Sentence(document, sent.start, sent.finish)
        try:
            sentence.lang = detect(sentence.text)
        except LangDetectException:
            pass
        document.sentences.append(sentence)
"""


class Processor:
    def __init__(self, cores: Optional[List[CoreBase]] = None):
        if not cores:
            cores = [FallbackCore()]
        self.cores = cores

    def core_selector(self, doc: Document, text_process_params: TextProcessParams) -> Optional[CoreBase]:
        for core in self.cores:
            if core.can_process(doc, text_process_params):
                return core
        return None

    def process_text(self, text: str, text_process_params: TextProcessParams) -> Document:
        result: Document = Document(text)

        try:
            total_letters = sum(c.isalpha() for c in text)
            if total_letters < 50:
                result.warnings.append(MessageWithCode(1, f"Text is too short - only {total_letters} letters found."))

            langs: List[Language] = sorted(detect_langs(text[:100000]), key=lambda l: l.prob, reverse=True)
            if len(langs) == 0:
                result.errors.append(MessageWithCode(1, "Cannot determine text language."))
                return result

            main_lang: Language = langs[0]
            if main_lang.prob < 0.6:
                result.warnings.append(MessageWithCode(2, f"Main language {main_lang.lang} is determined with " +
                                                       f"small confidence ({main_lang.prob})."))

            result.main_lang = main_lang.lang
            result.logs.append('Main document language detected as "{}"'.format(main_lang.lang))

            selected_core: Optional[CoreBase] = self.core_selector(result, text_process_params)

            if selected_core is None:
                result.errors += MessageWithCode(2, f"Cannot process detected language '{main_lang.lang}'")
                return result

            result.logs.append('"{}" core selected for further processing'.format(type(selected_core).__name__))

            selected_core.process_document(result, text_process_params)
        except Exception as ex:
            result.errors.append(MessageWithCode(3, "Internal digest_processor error:\n" + str(ex)))

        return result
