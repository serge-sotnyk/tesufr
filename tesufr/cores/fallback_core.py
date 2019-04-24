import re
from collections import defaultdict
from typing import List, Dict

from ..models import Entity, EntityKind, Fragment
from .core_base import CoreBase
from .core_utils import parse_sentences
from .. import TextProcessParams
from ..models import Document


class FallbackCore(CoreBase):
    """Fallback core"""

    def _retrieve_kw(self, doc: Document, text_process_params: TextProcessParams):
        kw_candidates: Dict[str, List[Fragment]] = defaultdict(list)
        p = re.compile(r'\w+')
        for w in p.finditer(doc.text):
            key = w.group().casefold()
            if len(key) < 4:
                continue
            kw_candidates[key].append(Fragment(doc, w.start(), w.end()))
        kw_list = sorted(kw_candidates.items(), key=lambda i: len(i[1]), reverse=True)
        kw_list = kw_list[:text_process_params.keywords_number]
        for key, entries in kw_list:
            e = Entity(str(entries[0]), EntityKind.KEYWORD)
            e.entries = entries
            doc.keywords.append(e)

    def can_process(self, doc: Document, text_process_params: TextProcessParams) -> bool:
        # This core can process any language and params
        return True

    def __init__(self):
        ...

    def process_document(self, doc: Document, text_process_params: TextProcessParams):
        doc.keywords.clear()
        doc.entities.clear()

        parse_sentences(doc)
        for i, s in zip(range(text_process_params.summary_size.calculate_size(len(doc.sentences))), doc.sentences):
            summary_sent = Entity(s.text, EntityKind.SUMMARY_SENTENCE)
            summary_sent.entries.append(s)
            doc.summary.append(summary_sent)

        self._retrieve_kw(doc, text_process_params)
