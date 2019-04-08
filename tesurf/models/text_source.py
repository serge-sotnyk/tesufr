import abc


class TextSource:
    @property
    @abc.abstractmethod
    def text(self) -> str:
        """This method should be overridden in subclasses"""
        raise NotImplementedError
