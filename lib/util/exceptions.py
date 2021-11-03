class InvalidDotenvFileError(ValueError):
    def __init__(self, reason):
        self.strerr = reason