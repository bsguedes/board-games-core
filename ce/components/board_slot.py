from ce.components.token_tray import TokenTray


class BoardSlot:
    def __init__(self):
        self.card = None
        self.cached = 0
        self.cash = 0
        self.tokens = TokenTray()
