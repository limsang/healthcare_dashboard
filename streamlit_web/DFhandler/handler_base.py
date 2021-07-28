from abc import *

class BaseHandler(metaclass=ABCMeta):

    @abstractmethod
    def load_from_csv(self):
        pass

    @abstractmethod
    def preproc(self):
        pass

    @abstractmethod
    def analysis(self):
        pass




