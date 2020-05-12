from base_common import rand_id_gen


class PlayerBase:
    def __init__(self, player_name):
        self.name: str = player_name
        self.secret: str = rand_id_gen()
        self.ping: int = 0
