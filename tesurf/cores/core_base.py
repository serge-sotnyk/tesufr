from abc import ABC, abstractmethod

from .. import TextProcessParams
from ..models import Document


class CoreBase(ABC):
    """Base class for different annotating cores"""

    @abstractmethod
    def process_document(self, doc: Document, text_process_params: TextProcessParams):
        pass
