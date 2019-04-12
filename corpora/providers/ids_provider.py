from abc import ABC

from sklearn.model_selection import train_test_split

from corpora import ProviderBase, SetType


class IdsProvider(ProviderBase, ABC):
    """
    Abstract implementation of corpus provider, which can read all documents identifiers at initialization stage
    """

    def __init__(self):
        self.ids = []

    def _prepare_subsets(self, dev_part: float = 0.2, test_part: float = 0.2, random_state=1974):
        assert dev_part >= 0
        assert test_part >= 0
        assert dev_part + test_part <= 1
        dev_part_wo_test = dev_part/(1-test_part)
        train_ids, test_ids = train_test_split(self.ids, test_size=test_part, random_state=random_state)
        train_ids, dev_ids = train_test_split(train_ids, test_size=dev_part_wo_test, random_state=random_state)
        self.ids_train = train_ids
        self.ids_dev = dev_ids
        self.ids_test = test_ids

    def subset_size(self, type_of_set: SetType) -> int:
        if type_of_set == SetType.ALL:
            return len(self.ids)
        elif type_of_set == SetType.TRAINING:
            return len(self.ids_train)
        elif type_of_set == SetType.DEV:
            return len(self.ids_dev)
        elif type_of_set == SetType.TEST:
            return len(self.ids_test)
        else:
            raise NotImplementedError()