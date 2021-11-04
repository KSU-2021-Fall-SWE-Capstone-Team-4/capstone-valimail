class InvalidDotenvFileError(ValueError):
    def __init__(self, reason):
        self.strerr = reason

class UndefinedVariableError(ValueError):
    def __init__(self, reason):
        self.strerr = reason