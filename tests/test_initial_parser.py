from tesufr import *


def test_parse_paragraphs_basic():
    text = "Paragraph 1. Sentence 2.\r\nParagraph 2"
    paragraphs = parse_paragraphs(text)
    assert len(paragraphs) == 2


def test_parse_paragraphs_different_delimiters():
    text = 'Sentence 2\nthe sentence 3.'
    paragraphs = parse_paragraphs(text)
    assert len(paragraphs) == 2
    text = 'Sentence 2\r\nthe sentence 3.'
    paragraphs = parse_paragraphs(text)
    assert len(paragraphs) == 2
    text = 'Sentence 2\n\rthe sentence 3.'
    paragraphs = parse_paragraphs(text)
    assert len(paragraphs) == 2
    text = 'Sentence 2\rthe sentence 3.'
    paragraphs = parse_paragraphs(text)
    assert len(paragraphs) == 2


def test_parse_paragraphs_trimming():
    text = "\r\nParagraph 1. Sentence 2.  \r\n   Paragraph 2\r\r\r"
    paragraphs = parse_paragraphs(text)
    assert len(paragraphs) == 2
    assert text_fragment(text, paragraphs[0]) == "Paragraph 1. Sentence 2."
    assert text_fragment(text, paragraphs[1]) == "Paragraph 2"


def test_parse_sentences_multilingual():
    text = '''A sentences (sentence 0).
    Sentence 1. Sentence 2
the sentence 3. Sentence 4!!! Sentence 5?
The last sentence (#6)...
           '''
    sentences = parse_sentences_multilingual(text)
    texts = [text_fragment(text, pos) for pos in sentences]
    assert len(sentences) == 7

