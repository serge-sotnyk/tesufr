from spacy.tokens import Span, Token
from spacy.tokens.doc import Doc
from summa import summarizer

from ...models import MessageWithCode
from ... import TextProcessParams
from ...models import Document, Entity, EntityKind, Sentence, Fragment
from ..core_base import CoreBase
from ...initial_parser import text_fragment, FragmentPositions, parse_paragraphs
from collections import namedtuple, defaultdict
from typing import Dict, List, NamedTuple
import spacy
from functools import lru_cache
from bpemb import BPEmb
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import re


class LangModelDefinition(NamedTuple):
    lang: str
    spacy_vocab_name: str
    summa_lang: str


lang_models: Dict[str, LangModelDefinition] = {
    'en': LangModelDefinition('en', 'en_core_web_sm', 'english'),
    'de': LangModelDefinition('de', 'de_core_news_sm', 'german'),
    'fr': LangModelDefinition('fr', 'fr_core_news_sm', 'french'),
    'it': LangModelDefinition('it', 'it_core_news_sm', 'italian'),
}

_ImportanceIndex = namedtuple("_ImportanceIndex", ['importance', 'index'])
_NeKey = namedtuple("_NeKey", ['lemma', 'subtype'])

_re_tokenizer = re.compile(r"\w+", re.UNICODE)

_diversity_factor: float = 0.25


def can_process_lang(lang: str) -> bool:
    return lang in lang_models


class EmCore(CoreBase):
    """Annotation core based on spacy parser, pos tagger"""

    def __init__(self, lang: str):
        if not can_process_lang(lang):
            raise ValueError(f"'{lang}' is not valid language id.")
        self.lang_model_definition = lang_models[lang]
        self.nlp = spacy.load(self.lang_model_definition.spacy_vocab_name)
        self.bpemb = BPEmb(lang=lang, dim=300)

    def can_process(self, doc: Document, text_process_params: TextProcessParams) -> bool:
        return True if doc.main_lang == self.lang_model_definition.lang else False

    def _vectorize_entity(self, entity: Entity, kw: Span):
        vector = np.zeros((1, self.bpemb.dim), dtype='float32')
        counter = 0
        for t in kw:
            if not t.is_stop:
                w_vector = self.bpemb.embed(t.lemma_).sum(axis=0)
                vector += w_vector
                counter += 1
        if counter > 1:
            vector /= counter
        entity.vector = vector

    def _vectorize_sent(self, sent: Sentence, sp_sent: Span):
        vector = np.zeros((1, self.bpemb.dim), dtype='float32')
        counter = 0
        processable_pos = {'NOUN', 'PROPN', 'ADJ', 'VERB'}
        stop_words = self.nlp.Defaults.stop_words
        for t in sp_sent:
            if t.pos_ not in processable_pos:
                continue
            if t.is_stop or t.lower_ in stop_words or t.lemma_ in stop_words:
                continue
            w_vector = self.bpemb.embed(t.lemma_).sum(axis=0)
            vector += w_vector
            counter += 1
        if counter > 1:
            vector /= counter
        sent.embedding = vector

    @staticmethod
    def _count_tokens(kw: Entity) -> int:
        matches = _re_tokenizer.findall(kw.lemma)
        return len(matches)

    @staticmethod
    def _get_kw_indices(doc_vector: np.ndarray,
                        kw_candidates: List[Entity],
                        kw_num: int,
                        diversity_factor: float) -> List[int]:
        """ Method selects indices of keywords in kw_candidates list.
        Prototype: _MMR in https://github.com/swisscom/ai-research-keyphrase-extraction/blob/master/swisscom_ai/research_keyphrase/model/method.py
        original article: https://arxiv.org/pdf/1801.04470.pdf

        :param doc_vector: numpy array document embeddings.
        :param kw_candidates: list with candidates to keywords. Items has @Entity type.
        :param kw_num: number of desired keywords.
        :param diversity_factor: control tradeoff between informativeness and diversity [0..1]
        """
        if kw_num == 0 or kw_num is None:
            kw_num = 10
        kw_num = min(kw_num, len(kw_candidates))
        if kw_num == 0:
            return []
        if kw_num >= len(kw_candidates):
            return list(range(kw_num))

        kw_vectors_nd = np.vstack([entity.vector for entity in kw_candidates])
        selected_candidates = []
        unselected_candidates = [c for c in range(len(kw_candidates))]

        # select the first keyword
        kw_distances = cosine_similarity(doc_vector, kw_vectors_nd)
        kw_distances_1d = np.reshape(kw_distances, (kw_distances.shape[1]))
        selected: int = np.argmax(kw_distances_1d)
        selected_candidates.append(selected)
        unselected_candidates.remove(selected)
        kw_counter = EmCore._count_tokens(kw_candidates[selected])

        # select other N-1 keywords
        for _ in range(kw_num - 1):
            kw_vectors_selected_nd = np.vstack([kw_candidates[ind].vector for ind in selected_candidates])
            kw_vectors_unselected_nd = np.vstack([kw_candidates[ind].vector for ind in unselected_candidates])
            similarities = cosine_similarity(kw_vectors_unselected_nd, kw_vectors_selected_nd)
            max_similarity_per_unselected = np.max(similarities, axis=1)
            ranks = []
            for i, unselected_ind in enumerate(unselected_candidates):
                doc_sim = kw_distances_1d[unselected_ind]
                max_kw_sim = max_similarity_per_unselected[i]
                rank = (1 - diversity_factor) * doc_sim - diversity_factor * max_kw_sim
                ranks.append(rank)
            selected = unselected_candidates[np.argmax(ranks)]
            selected_candidates.append(selected)
            unselected_candidates.remove(selected)
            kw_counter += EmCore._count_tokens(kw_candidates[selected])
            if kw_counter >= kw_num:
                break

        return selected_candidates

    def _extract_keywords(self, doc: Document, kw_candidates, kw_num: int):
        res = {}
        for fragment, kw in kw_candidates:
            lemma: str = kw.lemma_
            if lemma not in res:
                entity = Entity(lemma, EntityKind.KEYWORD)
                res[lemma] = entity
                self._vectorize_entity(entity, kw)
            entity = res[lemma]
            entity.entries.append(fragment)

        entities = list(res.values())

        doc_vector = np.zeros((1, self.bpemb.dim), dtype='float32')
        count = 0
        for entity in entities:
            doc_vector += entity.vector * len(entity.entries)
            count += len(entity.entries)
        if count > 1:
            doc_vector /= count

        doc.embedding = doc_vector

        kw_indices = self._get_kw_indices(doc_vector, entities, kw_num, _diversity_factor)
        doc.keywords += [entities[ind] for ind in kw_indices]

    def _find_noun_chunks(self, sent: Span) -> List[Span]:
        result = []

        def add_buff_to_result(buff: List[Token]):
            if len(buff) > 0:
                doc: Doc = buff[0].doc
                start = buff[-1].idx
                end = buff[0].idx + len(buff[0])
                result.append(doc.char_span(start, end))
                buff.clear()

        nouns = {'NOUN', 'PROPN'}
        stop_words = self.nlp.Defaults.stop_words
        buff = []
        for t in reversed(sent):
            if t.is_stop or t.lower_ in stop_words or t.lemma_ in stop_words or len(t) < 3:
                add_buff_to_result(buff)
                continue
            if t.pos_ in nouns:
                if len(buff) > 0 and buff[-1].pos_ not in nouns:
                    add_buff_to_result(buff)
                buff.append(t)
                continue
            if len(t) > 0 and t.pos_ == 'ADJ':
                buff.append(t)
                continue
            add_buff_to_result(buff)
            add_buff_to_result(buff)
        add_buff_to_result(buff)  # maybe buffer is not empty
        return result

    @staticmethod
    def _extract_textrank_digest(doc: Document, summary_size: int):
        sent_len = len(doc.sentences)
        sim_mat = np.zeros([sent_len, sent_len])
        for y in range(sent_len):
            for x in range(y + 1, sent_len):
                sim = max(0.0001, cosine_similarity(doc.sentences[x].embedding, doc.sentences[y].embedding))
                sim_mat[y][x] = sim
                sim_mat[x][y] = sim_mat[y][x]
        for x in range(sent_len):
            sim_mat[x] /= sim_mat[x].sum()
        nx_graph = nx.from_numpy_array(sim_mat)
        try:
            scores = nx.pagerank(nx_graph)
        except nx.PowerIterationFailedConvergence as ex:
            doc.warnings.append(MessageWithCode(3, "Exception PowerIterationFailedConvergence - cannot calculate "
                                                   "TextRank matrix, fallback is used."))
            filtered_indices = range(summary_size)
        else:
            ranged_importances: List[_ImportanceIndex] = []
            for i in range(sent_len):
                doc.sentences[i].importance = scores[i]
                ranged_importances.append(_ImportanceIndex(scores[i], i))
            ranged_importances = sorted(ranged_importances, key=lambda x: x.importance, reverse=True)
            filtered_indices: List[int] = sorted([ri.index for ri in ranged_importances[:summary_size]])
        doc.summary.clear()
        for i in filtered_indices:
            entity = Entity(str(doc.sentences[i]), EntityKind.SUMMARY_SENTENCE)
            entity.entries.append(doc.sentences[i])
            doc.summary.append(entity)

    def process_document(self, doc: Document, text_process_params: TextProcessParams):
        doc.sentences.clear()
        doc.keywords.clear()
        doc.entities.clear()

        paragraphs: List[FragmentPositions] = parse_paragraphs(doc.text)
        kw_candidates = []
        entities = defaultdict(list)
        for p in paragraphs:
            paragraph_text = text_fragment(doc.text, p)
            pp = self.nlp(paragraph_text)
            for sent in pp.sents:
                doc_sent = Sentence(doc, p.start + sent.start_char,
                                    p.start + sent.end_char, self.lang_model_definition.lang)
                self._vectorize_sent(doc_sent, sent)
                doc.sentences.append(doc_sent)

                kw_candidates += [(Fragment(doc, p.start + kw.start_char, p.start + kw.end_char), kw)
                                  for kw in self._find_noun_chunks(sent)]
            for en in pp.ents:
                en_key = _NeKey(en.lemma_, en.label_)
                entities[en_key].append(Fragment(doc, p.start + en.start_char, p.start + en.end_char))

        # self._extract_textrank_digest(doc,
        #                              text_process_params.summary_size.calculate_size(len(doc.sentences)))
        self._extract_keywords(doc, kw_candidates, text_process_params.keywords_number)

        # Extract summary
        ratio = text_process_params.summary_size.calculate_ratio(len(doc.sentences))
        summary = summarizer.summarize(doc.text, ratio=ratio, language=self.lang_model_definition.summa_lang)
        for s in summary.splitlines():
            doc.summary.append(Entity(s, EntityKind.SUMMARY_SENTENCE))

        for en_key, entries in entities.items():
            ent = Entity(en_key.lemma, EntityKind.NAMED, en_key.subtype)
            ent.entries += entries
            doc.entities.append(ent)


@lru_cache(typed=True)
def construct_em_core(lang: str) -> EmCore:
    return EmCore(lang)
