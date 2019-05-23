import os
from typing import Iterable, List
from zipfile import ZipFile

from ... import parse_sentences_multilingual
from tesufr.corpora import SetType, CorpusDocument, CorpusPurpose
from tesufr.text_utils import preprocess_pdf
from tesufr.text_utils.dos_formatting import remove_dos_formatting
from .ids_provider import IdsProvider


class Krapivin2009Provider(IdsProvider):
    """
    Provider for
    Mikalai Krapivin and Aliaksandr Autayeu and Maurizio Marchese, "Large Dataset for Keyphrases Extraction",
    Technical Report DISI-09-055, DISI, University of Trento, Italy, 2009
    """

    @staticmethod
    def _extract_article_summary_krapivin2009(article: str) -> (str, List[str]):
        summary = []
        text = []
        in_abstract, in_text, in_title = False, False, False
        for l in article.splitlines():
            if l.startswith('--') and len(l) == 3:
                if l.endswith('T'):
                    in_abstract, in_text, in_title = False, False, True
                elif l.endswith('B'):
                    in_abstract, in_text, in_title = False, True, False
                    text.append('')  # After title
                elif l.endswith('A'):
                    in_abstract, in_text, in_title = True, False, False
                else:
                    in_abstract, in_text, in_title = False, False, False
            else:
                if in_abstract:
                    sents = parse_sentences_multilingual(l)
                    for sent in sents:
                        summary.append(l[sent.start:sent.finish])
                if in_text:
                    text.append(l)

        #text_str = remove_dos_formatting('\n'.join(text))
        text_str = preprocess_pdf('\n'.join(text))

        return text_str, summary

    def purpose(self) -> CorpusPurpose:
        return CorpusPurpose(CorpusPurpose.SUMMARY | CorpusPurpose.KEYWORDS)

    def subset(self, type_of_set: SetType) -> Iterable[CorpusDocument]:
        if type_of_set == SetType.ALL:
            ids = self.ids
        elif type_of_set == SetType.TRAINING:
            ids = self.ids_train
        elif type_of_set == SetType.DEV:
            ids = self.ids_dev
        elif type_of_set == SetType.TEST:
            ids = self.ids_test
        else:
            raise NotImplementedError()

        for id_ in ids:
            yield self.document_by_id(id_)

    def document_by_id(self, id_: str) -> CorpusDocument:
        lang = self.language()
        with ZipFile(self.filename) as zip_corpus:
            with zip_corpus.open('all_docs_abstacts_refined/' + id_ + '.txt') as a:
                raw_article = a.read().decode(encoding='utf-8', errors='replace')
            with zip_corpus.open('all_docs_abstacts_refined/' + id_ + '.key') as kw:
                raw_kw = kw.read().decode(encoding='utf-8', errors='replace')
        article, summary = Krapivin2009Provider._extract_article_summary_krapivin2009(raw_article)
        res = CorpusDocument(id_, text=article,
                             ref_summary=summary,
                             ref_keywords=raw_kw.splitlines(),
                             lang=lang)
        return res

    def __init__(self, local_filename: str = 'corpora_data/krapivin2009.zip',
                 url: str = 'https://drive.google.com/uc?export=download&confirm=5CKR&id=1zRP0sKH0tn3P2hWRyE2E3yXjjbkYLHtR'):
        super().__init__()
        self.filename = os.path.abspath(local_filename)
        if not self.check_if_file_exist_make_dir(self.filename):
            self.download_with_progress(url, self.filename)

        with ZipFile(self.filename) as zip_corpus:
            all_names = zip_corpus.namelist()
        prefix = 'all_docs_abstacts_refined/'
        suffix = '.txt'
        ids = [s[len(prefix):-len(suffix)] for s in all_names if s.startswith(prefix) and s.endswith(suffix)]
        self.ids = sorted(ids)
        self._prepare_subsets()
