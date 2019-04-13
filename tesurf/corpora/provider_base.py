import os
import urllib.parse as urlparse
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable

import requests
from google_drive_downloader import GoogleDriveDownloader as gdd
from tqdm.auto import tqdm

from .corpus_document import CorpusDocument
from .corpus_purposes import CorpusPurpose
from .set_types import SetType


class ProviderBase(ABC):
    """
    Abstract base class for corpus providers
    """
    def language(self) -> str:
        """Returns language (two-letter string) of the corpus documents."""
        return 'en'

    def subset_size(self, type_of_set: SetType) -> int:
        """Returns length of documents subset."""
        # dumb implementation, recommended to implement optimized edition in descendants
        return sum(1 for d in self.subset(type_of_set))

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
        if link.startswith('https://drive.google.com'):
            # special version for Google Drive
            parsed = urlparse.urlparse(link)
            file_id = urlparse.parse_qs(parsed.query)['id']
            gdd.download_file_from_google_drive(file_id, filename, unzip=False)
            return

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
