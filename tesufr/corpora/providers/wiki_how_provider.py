import os
from typing import Iterable
from zipfile import ZipFile

from tesufr.corpora import SetType, CorpusDocument, CorpusPurpose
from .ids_provider import IdsProvider


class WikiHowProvider(IdsProvider):
    """
    Provider for
    WikiHow: A Large Scale Text Summarization Dataset
    WikiHow is a new large-scale dataset using the online WikiHow (http://www.wikihow.com/) knowledge
       base. The dataset is introduced in https://arxiv.org/abs/1810.09305. Please refer to the paper
       for more information regarding the dataset and its properties.
    """

    def purpose(self) -> CorpusPurpose:
        return CorpusPurpose(CorpusPurpose.SUMMARY)

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
        with self.zip_corpus.open('articles/' + id_ + '.txt') as a:
            raw_article = a.read().decode(encoding='utf-8', errors='replace')
        summary, article = raw_article.split('\n@article\n')
        res = CorpusDocument(id_, text=article,
                             ref_summary=summary.splitlines(),
                             ref_keywords=[],
                             lang=lang)
        return res

    def __init__(self, local_filename: str = 'corpora_data/WikiHow.zip',
                 url: str = 'https://github.com/serge-sotnyk/tesufr/releases/download/v0.0.1/WikiHow.zip'):
        super().__init__()
        self.filename = os.path.abspath(local_filename)
        if not self.check_if_file_exist_make_dir(self.filename):
            self.download_with_progress(url, self.filename)

        self.zip_corpus = ZipFile(self.filename)
        all_names = self.zip_corpus.namelist()
        prefix = 'articles/'
        suffix = '.txt'
        ids = [s[len(prefix):-len(suffix)] for s in all_names if s.startswith(prefix) and s.endswith(suffix)]
        self.ids = sorted(ids)
        self._prepare_subsets()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._close(manual_close=False)

    def _close(self, manual_close: bool):
        if self.zip_corpus is not None:
            self.zip_corpus.close()
            self.zip_corpus = None

    def close(self):
        self._close(True)
