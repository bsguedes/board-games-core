from base_common import to_dict
from base_state import PlayerState
from base_player import PlayerBase
from ce.components.objective_board import ObjectiveBoard
from ce.components.deck import Deck
from ce.components.stage import Stage
from ce.player import CEPlayer
from typing import List


class CECommonState(PlayerState):
    def __init__(self, player: PlayerBase, current_player: PlayerBase,
                 deck: Deck, bonus_num: int, obj_board: ObjectiveBoard,
                 stage: Stage, player_objects: List[CEPlayer]):
        self.deck: Deck = deck
        self.bonus_deck_count: int = bonus_num
        self.objective_board: ObjectiveBoard = obj_board
        self.stage: Stage = stage
        self.player_objects: List[CEPlayer] = player_objects
        self.ce_player: CEPlayer = next(p for p in self.player_objects if p.player == player)
        PlayerState.__init__(self, player, current_player)

    def as_dict_game(self):
        payload = {
            'DeckCount': self.deck.number_of_cards(),
            'Contracts': [c.ID for c in self.deck.contracts],
            'BonusDeckCount': self.bonus_deck_count,
            'ObjectiveBoard': [o.ID for o in self.objective_board.round_objectives],
            'Stage': {
                'OnStage': [d.upper_face for d in self.stage.on_stage],
                'OffStage': len(self.stage.off_stage),
                'CanReroll': self.stage.can_reroll()
            },
            'Opponents': [{
                'Player': p.player.name,
                'Champion': p.champion.Name,
                'Talents': to_dict(p.talents),
                'HandCount': len(p.hand),
                'Board': to_dict(p.board),
                'BonusCardCount': len(p.bonus_cards)
            } for p in self.player_objects if p != self.ce_player],
            'Player': {
                'Champion': self.ce_player.champion.Name,
                'Talents': to_dict(self.ce_player.talents),
                'Hand': [c.ID for c in self.ce_player.hand],
                'Board': to_dict(self.ce_player.board),
                'BonusCards': [c.ID for c in self.ce_player.bonus_cards]
            }
        }
        return payload

    def your_options_game(self):
        pass
