import os
from typing import Iterable
from zipfile import ZipFile

from sklearn.model_selection import train_test_split

from corpora import SetType, CorpusDocument, CorpusPurpose
from .. import ProviderBase


class BbcNewsProvider(ProviderBase):
    """
    Provider for https://www.kaggle.com/pariza/bbc-news-summary/data corpora
    """

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
                res = CorpusDocument(id_, text=article, ref_summary=summary.splitlines(), lang=lang)
                yield res

    def __init__(self,
                 local_filename: str = 'corpora/bbc-news-summary.zip',
                 url: str = 'https://drive.google.com/uc?authuser=0&id=1xtY-OYYoyeat_DS_Jw-DdCT5MCmC44qV&export=download'):
        self.filename = os.path.abspath(local_filename)
        if not self.check_if_file_exist_make_dir(self.filename):
            self.download_with_progress(url, self.filename)

        with ZipFile(self.filename) as zip_corpus:
            all_names = zip_corpus.namelist()
        prefix = 'Summaries/'
        ids = [s[len(prefix):] for s in all_names if s.startswith(prefix) and not s.endswith('/')]
        self.ids = sorted(ids)
        train_ids, test_ids = train_test_split(self.ids, test_size=0.2, random_state=1974)
        train_ids, dev_ids = train_test_split(train_ids, test_size=0.25, random_state=1974)  # 20% of the full set
        self.ids_train = train_ids
        self.ids_dev = dev_ids
        self.ids_test = test_ids
