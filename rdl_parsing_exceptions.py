import abc
from abc import ABC


class TransformationException(Exception, ABC):
    @abc.abstractmethod
    def exception_description(self):
        pass


class RDLTransformationException(TransformationException):
    def __init__(self):
        super(RDLTransformationException, self).__init__()
        rdl_syntax_error = None

    def exception_description(self):
        return ""


class RDLSyntaxRelatedTransformationException(RDLTransformationException):
    def __init__(self, syntax_error):
        super().__init__()
        self.syntax_error = syntax_error

    def exception_description(self):
        return self.syntax_error.str()

