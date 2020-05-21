from ce.components.token_tray import TokenTray
from ce.components.card import Card


class BoardSlot:
    def __init__(self):
        self.card: Card = None
        self.cached: int = 0
        self.cash: int = 0
        self.tokens: TokenTray = TokenTray()
