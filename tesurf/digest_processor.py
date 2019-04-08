from langdetect.lang_detect_exception import LangDetectException

from .initial_parser import parse_sentences_multilingual
from .models import Document, Fragment, Sentence, MessageWithCode
from .text_process_params import TextProcessParams
# from .lang_cores import can_process_lang, construct_spacy_core, CoreBase
from langdetect import detect, detect_langs
from langdetect.language import Language
from typing import List


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


class DigestProcessor:
    def __init__(self):
        pass

    def process_text(self, text: str, text_process_params: TextProcessParams) -> Document:
        result: Document = Document(text)

        try:
            total_letters = sum(c.isalpha() for c in text)
            if total_letters < 50:
                result.warnings.append(MessageWithCode(1, f"Text is too short - only {total_letters} letters found."))

            langs: List[List[Language]] = sorted(detect_langs(text), key=lambda l: l.prob, reverse=True)
            if len(langs) == 0:
                result.errors.append(MessageWithCode(1, "Cannot determine text language."))
                return result

            main_lang: Language = langs[0]
            if main_lang.prob < 0.6:
                result.warnings.append(MessageWithCode(2, f"Main language {main_lang.lang} is determined with " +
                                                       f"small confidence ({main_lang.prob})."))

            selected_core: CoreBase = None

            if can_process_lang(main_lang.lang):
                selected_core = construct_spacy_core(main_lang.lang)

            if selected_core is None:
                result.errors += MessageWithCode(2, f"Cannot process detected language '{main_lang.lang}'")
                return result

            selected_core.process_document(result, text_process_params)
        except Exception as ex:
            result.errors.append(MessageWithCode(2, "Internal digest_processor error:\n"+str(ex)))

        return result
