from collections import defaultdict
from typing import List

from .core_base import CoreBase
from .. import TextProcessParams
from ..initial_parser import FragmentPositions, parse_paragraphs
from ..models import Document


class FallbackCore(CoreBase):
    """Fallback core"""

    def __init__(self):
        ...

    def process_document(self, doc: Document, text_process_params: TextProcessParams):
        doc.sentences.clear()
        doc.keywords.clear()
        doc.entities.clear()

        paragraphs: List[FragmentPositions] = parse_paragraphs(doc.text)
        kw_candidates = []
        entities = defaultdict(list)
