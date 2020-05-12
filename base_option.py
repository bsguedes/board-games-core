from base_common import rand_id_gen
from typing import Dict, Any


class OptionBase:
    def __init__(self, option: Dict):
        self.OptionCode: str = rand_id_gen()
        self.Option: Dict[str, Any] = option
