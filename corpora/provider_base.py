from abc import ABC, abstractmethod
from typing import Iterable

from corpora.corpus_document import CorpusDocument
from corpora.corpus_purposes import CorpusPurpose
from corpora.set_types import SetType

import os
from pathlib import Path
import math

import requests
from tqdm.auto import tqdm


class ProviderBase(ABC):
    """
    Abstract base class for corpus providers
    """

    def language(self) -> str:
        """Return language (two-letter string) of the corpus documents."""
        return 'en'

    @abstractmethod
    def purpose(self) -> CorpusPurpose:
        """
        Method returns purpose of the corpus (keywords/keyphrases or summary) or combination of flags.
        """
        raise NotImplementedError()

    @abstractmethod
    def subset(self, type_of_set: SetType) -> Iterable[CorpusDocument]:
        """
        Method returns iterator for requested subset
        :param type_of_set: requested subset type
        :return: sequence with documents.
        """
        raise NotImplementedError()

    @staticmethod
    def check_if_file_exist_make_dir(filename: str) -> bool:
        """
        Function performs the following checks:
           if file directory does not exist, directory is created.
        :param filename: name of a new file.
        :return: boolean sign if file is already existed.
        """
        file_path = Path(filename)
        dir_ = str(file_path.parent.absolute())
        if not os.path.exists(dir_):
            os.mkdir(dir_)
        return file_path.is_file()

    @staticmethod
    def download_with_progress(link: str, filename: str):
        file_path = Path(filename)

        dir_ = str(file_path.parent.absolute())
        if not os.path.exists(dir_):
            os.mkdir(dir_)

        if file_path.is_file():
            print(f"File '{file_path.absolute()}' is already existed, downloading was skipped.")
            return

        with open(filename, "wb") as f:
            print("Downloading '%s'" % filename)
            response = requests.get(link, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None:  # no content length header
                print(f"Length of the downloaded file is unknown, start downloading")
                f.write(response.content)
            else:
                wrote = 0
                total_size: int = int(total_length)
                chunk_size = 1024 * 8
                with tqdm(total=total_size, unit="B") as p_bar:
                    for data in response.iter_content(chunk_size=chunk_size):
                        bl_size = f.write(data)
                        wrote += bl_size
                        p_bar.update(bl_size)

        print(f"File downloaded, length = {file_path.stat().st_size} b")
