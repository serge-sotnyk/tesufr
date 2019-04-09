from abc import ABC, abstractmethod, abstractclassmethod

from .. import TextProcessParams
from ..models import Document


class CoreBase(ABC):
    """Base class for different annotating cores"""

    @abstractmethod
    def process_document(self, doc: Document, text_process_params: TextProcessParams):
        ...

    @abstractmethod
    def can_process(self, doc: Document, text_process_params: TextProcessParams) -> bool:
        ...
