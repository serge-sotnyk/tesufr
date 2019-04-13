from .summary_size import SummarySize
from .text_process_params import TextProcessParams
from .processor import Processor
from .initial_parser import parse_paragraphs, parse_sentences_multilingual, FragmentPositions, text_fragment

__version__: str = "0.0.1"


def version():
    return __version__
