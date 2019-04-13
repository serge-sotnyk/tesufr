import os
from typing import Iterable, Sequence
from zipfile import ZipFile

from .. import SetType, CorpusDocument, CorpusPurpose
from .ids_provider import IdsProvider


class BbcNewsProvider(IdsProvider):
    """
    Provider for https://www.kaggle.com/pariza/bbc-news-summary/data corpora
    """

    @staticmethod
    def _bbc_sentences_divider(text: str) -> Sequence[str]:
        start = 0

        def fetch_sent(pos: int) -> str:
            nonlocal start
            res = text[start: pos + 1].strip()
            start = pos + 1
            return res

        puncts = {'.', '!', '?'}

        tlen = len(text)
        for pos in range(tlen - 1):
            if text[pos] in puncts:
                if text[pos + 1].isspace() or text[pos + 1].isupper():
                    yield fetch_sent(pos)
                elif pos + 2 < tlen and text[pos + 1] == '"':
                    if text[pos + 2].isupper() or text[pos + 2].isspace():
                        yield fetch_sent(pos + 1)
        yield fetch_sent(len(text) - 1)

    def purpose(self) -> CorpusPurpose:
        return CorpusPurpose.SUMMARY

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

        lang = self.language()
        with ZipFile(self.filename) as zip_corpus:
            for id_ in ids:
                with zip_corpus.open('News Articles/' + id_) as a:
                    article = a.read().decode(encoding='utf-8', errors='replace')
                with zip_corpus.open('Summaries/' + id_) as sm:
                    summary = sm.read().decode(encoding='utf-8', errors='replace')
                sum_sets = list(BbcNewsProvider._bbc_sentences_divider(summary))
                res = CorpusDocument(id_, text=article, ref_summary=sum_sets, lang=lang)
                yield res

    def __init__(self, local_filename: str = 'corpora_data/bbc-news-summary.zip',
                 url: str = 'https://drive.google.com/uc?authuser=0&id=1xtY-OYYoyeat_DS_Jw-DdCT5MCmC44qV&export=download'):
        super().__init__()
        self.filename = os.path.abspath(local_filename)
        if not self.check_if_file_exist_make_dir(self.filename):
            self.download_with_progress(url, self.filename)

        with ZipFile(self.filename) as zip_corpus:
            all_names = zip_corpus.namelist()
        prefix = 'Summaries/'
        ids = [s[len(prefix):] for s in all_names if s.startswith(prefix) and not s.endswith('/')]
        self.ids = sorted(ids)
        self._prepare_subsets()