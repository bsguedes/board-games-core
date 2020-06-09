class InvalidStateException(Exception):
    def __init__(self, state: str):
        self.state: str = state

    def __str__(self):
        return self.state
