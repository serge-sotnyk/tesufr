from tesufr import Processor, SummarySize, TextProcessParams
from tesufr.models import Document
from os import path
from nltk.corpus import udhr
import nltk

__location__ = path.dirname(__file__)

def test_digest_processor_en():
    processor = Processor()
    text = open(path.join(__location__, 'en_text.txt'), 'r', encoding='utf8').read()
    text_process_params = TextProcessParams(SummarySize.new_absolute(3), keywords_number=10)
    document = processor.process_text(text, text_process_params)
    assert isinstance(document, Document)
    assert len(document.sentences) >= 5

def test_digest_processor_it():
    processor = Processor()
    text = udhr.raw('Italian-Latin1')
    text_process_params = TextProcessParams(SummarySize.new_relative(0.1), keywords_number=10)
    document = processor.process_text(text, text_process_params)
    assert isinstance(document, Document)
    assert 5 <= len(document.sentences)

def test_digest_processor_de():
    processor = Processor()
    text = open(path.join(__location__, 'de_text.txt'), 'r', encoding='utf8').read()
    text_process_params = TextProcessParams(SummarySize.new_absolute(3), keywords_number=10)
    document = processor.process_text(text, text_process_params)
    assert isinstance(document, Document)
    assert 5 <= len(document.sentences)

def test_digest_processor_fr():
    processor = Processor()
    text = udhr.raw('French_Francais-Latin1')
    text_process_params = TextProcessParams(SummarySize.new_relative(0.1), keywords_number=10)
    document = processor.process_text(text, text_process_params)
    assert isinstance(document, Document)
    assert 5 <= len(document.sentences)
