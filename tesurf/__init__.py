from .digest_size import DigestSize
from .text_process_params import TextProcessParams
from .digest_processor import DigestProcessor
from .initial_parser import parse_paragraphs, parse_sentences_multilingual, FragmentPositions, text_fragment

__version__: str = "0.0.1"


def version():
    return __version__
