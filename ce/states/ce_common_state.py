from base_common import to_dict
from base_state import PlayerState
from base_player import PlayerBase
from ce.components.objective_board import ObjectiveBoard
from ce.components.deck import Deck
from ce.components.stage import Stage
from ce.player import CEPlayer
from typing import List, Dict, Any
from state_machine import GameState


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
            'Contracts': [None if c is None else c.ID for c in self.deck.contracts],
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
                'Board': {
                    'ChampionLevel': p.board.ChampionLevel,
                    'TopRow': [{
                        'Card': s.Card.ID if s.Card is not None else None,
                        'Cash': s.Cash,
                        'Cached': s.Cached,
                        'Talents': to_dict(s.Talents)
                    } for s in p.board.TopRow],
                    'MidRow': [{
                        'Card': s.Card.ID if s.Card is not None else None,
                        'Cash': s.Cash,
                        'Cached': s.Cached,
                        'Talents': to_dict(s.Talents)
                    } for s in p.board.MidRow],
                    'BotRow': [{
                        'Card': s.Card.ID if s.Card is not None else None,
                        'Cash': s.Cash,
                        'Cached': s.Cached,
                        'Talents': to_dict(s.Talents)
                    } for s in p.board.BotRow],
                },
                'BonusCardCount': len(p.bonus_cards),
                'Round': p.current_round,
                'Turn': p.current_turn
            } for p in self.player_objects if p != self.ce_player],
            'Player': {
                'Champion': self.ce_player.champion.Name,
                'Talents': to_dict(self.ce_player.talents),
                'Hand': [c.ID for c in self.ce_player.hand],
                'Board': {
                    'ChampionLevel': self.ce_player.board.ChampionLevel,
                    'TopRow': [{
                        'Card': s.Card.ID if s.Card is not None else None,
                        'Cash': s.Cash,
                        'Cached': s.Cached,
                        'Talents': to_dict(s.Talents)
                    } for s in self.ce_player.board.TopRow],
                    'MidRow': [{
                        'Card': s.Card.ID if s.Card is not None else None,
                        'Cash': s.Cash,
                        'Cached': s.Cached,
                        'Talents': to_dict(s.Talents)
                    } for s in self.ce_player.board.MidRow],
                    'BotRow': [{
                        'Card': s.Card.ID if s.Card is not None else None,
                        'Cash': s.Cash,
                        'Cached': s.Cached,
                        'Talents': to_dict(s.Talents)
                    } for s in self.ce_player.board.BotRow],
                },
                'BonusCards': [c.ID for c in self.ce_player.bonus_cards],
                'Round': self.ce_player.current_round,
                'Turn': self.ce_player.current_turn
            }
        }
        return payload

    def ce_apply_option(self, player: PlayerBase, ce_player: CEPlayer, option: Dict[str, Any]) -> List[GameState]:
        pass

    def your_options_game(self):
        pass
