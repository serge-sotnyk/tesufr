class SummarySize:
    """Size for summary in absolute of relative units (sentences)"""

    def __init__(self, is_relative: bool, relative_part: float = 0.0,
                 absolute_size: int = 0):
        self.__is_relative = is_relative
        if is_relative:
            if relative_part < 0:
                raise ValueError("Relative digest size should be non-negative value, but '{}' passed"
                                 .format(relative_part))
            self.__relative_part = relative_part
        else:
            if absolute_size < 0:
                raise ValueError("Absolute digest size should be non-negative value, but '{}' passed"
                                 .format(absolute_size))
            self.__absolute_size = absolute_size

    @property
    def is_relative(self):
        return self.__is_relative

    def calculate_size(self, total_sentences: int) -> int:
        if total_sentences < 0:
            raise ValueError("total_sentences should be non-negative value, but '{}' passed".format(total_sentences))
        if self.is_relative:
            result = int(round(total_sentences * self.__relative_part))
        else:
            result = self.__absolute_size
        return min(total_sentences, result)

    @staticmethod
    def new_relative(relative_part: float) -> 'SummarySize':
        return SummarySize(is_relative=True, relative_part=relative_part)

    @staticmethod
    def new_absolute(absolute_size: int) -> 'SummarySize':
        return SummarySize(is_relative=False, absolute_size=absolute_size)
