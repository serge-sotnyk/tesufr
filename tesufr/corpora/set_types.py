from enum import unique, Enum


@unique
class SetType(Enum):
    """
    Enumerates possible corpus subsets

    ALL      - Full documents set.
    TRAINING - Which you run your learning algorithm on.
    DEV      - Which you use to tune parameters, select features, and
               make other decisions regarding the learning algorithm. Sometimes also called the
               hold-out cross validation set.
    TEST     - Which you use to evaluate the performance of the algorithm, but not to make
               any decisions regarding what learning algorithm or parameters to use.
    """
    ALL = 'all'
    TRAINING = 'training'
    DEV = 'dev'
    TEST = 'test'
