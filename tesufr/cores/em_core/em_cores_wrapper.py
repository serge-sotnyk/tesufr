from tesufr import TextProcessParams
from tesufr.models import Document
from ...cores import CoreBase
from .em_core import construct_em_core, lang_models


class EmCoresWrapper(CoreBase):
    def process_document(self, doc: Document, text_process_params: TextProcessParams):
        main_lang = doc.main_lang
        core = construct_em_core(main_lang)
        return core.process_document(doc, text_process_params)

    def can_process(self, doc: Document, text_process_params: TextProcessParams) -> bool:
        main_lang = doc.main_lang
        if main_lang in lang_models:
            core = construct_em_core(main_lang)
            return core.can_process(doc, text_process_params)
        else:
            return False
