from collections import namedtuple
from typing import List
from textblob import TextBlob

FragmentPositions = namedtuple('SentencePos', 'start finish')
_paragraph_delimiters = {'\r', '\n'}


def trim_positions(text: str, start: int, finish: int)->(int, int):
    s = None
    f = None
    max_index = len(text)-1
    for pos in range(start, min(finish, max_index)):
        if not text[pos].isspace():
            s = pos
            break
    if s is None:
        # all characters are whitespace
        return None
    for pos in range(min(finish, max_index), start, -1):
        if not text[pos].isspace():
            f = pos+1
            break
    return s, f


def parse_paragraphs(text: str)->List[FragmentPositions]:
    # find all possible paragraph bounds
    paragraph_delimiter_positions = [i for i, c in enumerate(text) if c in _paragraph_delimiters]
    paragraph_delimiter_positions.insert(0, 0)
    paragraph_delimiter_positions.append(len(text))
    # filtrate consecutive delimiters
    start_paragraph_pos = 0
    paragraphs_pos = []
    for p in paragraph_delimiter_positions:
        if p <= start_paragraph_pos + 1:
            start_paragraph_pos = p
            continue
        trimmed_sent_pos = trim_positions(text, start_paragraph_pos, p)
        if trimmed_sent_pos:
            paragraphs_pos.append(FragmentPositions(trimmed_sent_pos[0], trimmed_sent_pos[1]))
        start_paragraph_pos = p

    return paragraphs_pos


def text_fragment(text: str, fragment_pos: FragmentPositions)->str:
    return text[fragment_pos.start: fragment_pos.finish]


def parse_sentences_multilingual(text: str)->List[FragmentPositions]:
    paragraphs = parse_paragraphs(text)
    res = []
    for paragraph in paragraphs:
        blob = TextBlob(text_fragment(text, paragraph))
        for sentence in blob.sentences:
            res.append(FragmentPositions(sentence.start+paragraph.start,
                                         sentence.end+paragraph.start))

    return res
