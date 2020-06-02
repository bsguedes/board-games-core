from game import Game
from random import shuffle, sample
from typing import List, Dict, Any
from base_player import PlayerBase
from ce.player import CEPlayer
from ce.states.ce_choose_resources import CEChooseResources
from ce.states.ce_player_turn import CEPlayerTurn
from ce.states.ce_draw_card import CEDrawCard
from ce.states.ce_draw_card_paying_money import CEDrawCardPayingMoney
from ce.states.ce_earn_money import CEEarnMoney
from ce.states.ce_earn_money_paying_talent import CEEarnMoneyPayingTalent
from ce.states.ce_play_card_pay_money import CEPlayCardPayMoney
from ce.states.ce_play_card_pay_talents import CEPlayCardPayTalents
from ce.states.ce_play_card_upgrade_champion import CEPlayCardUpgradeChampion
from ce.states.ce_take_talent import CETakeTalent
from ce.states.ce_take_talent_paying_card import CETakeTalentPayingCard
from ce.champions.champion import Channel
from ce.components.deck import Deck
from ce.components.stage import Stage
from ce.components.objective_board import ObjectiveBoard
from ce.components.bonus_deck import BonusDeck
from ce.db.loader import Loader
from state_machine import GameState
from exceptions import InvalidStateException

ROUNDS = 4
TURNS = 8


class ClassificacaoEtaria(Game):
    def __init__(self, parameters):
        Game.__init__(self, 'Classificação Etária', parameters)
        loader: Loader = Loader()
        self.deck: Deck = Deck(loader.Cards)
        self.bonus_cards: BonusDeck = BonusDeck(loader.Bonus)
        self.objective_board: ObjectiveBoard = ObjectiveBoard(loader.Objectives)
        self.stage: Stage = Stage()
        self.player_objects: List[CEPlayer] = []
        self.channels: List[Channel] = loader.Champions

    def setup_game(self):
        self.player_objects = [CEPlayer(player, sample(corp)[0]) for player, corp in zip(self.players, self.channels)]
        shuffle(self.player_objects)
        for ce_player in self.player_objects:
            ce_player.give_cards(self.deck.draw_cards(5))
            ce_player.give_bonus_cards(self.bonus_cards.draw_cards(2))
        for ce_player in self.player_objects:
            self.state_machine.add_to_end(GameState('ChooseResources', ce_player.player))
        n = len(self.player_objects)
        for i in range(ROUNDS):
            for j in range(TURNS - i):
                for k in range(n):
                    self.state_machine.add_to_end(GameState('PlayerTurn', self.player_objects[(k + i) % n].player))
        self.state_machine.add_to_end(GameState('Over', self.player_objects[0].player))

    def apply_option_on_current_state_game(self, player: PlayerBase, option: Dict[str, Any], state: GameState):
        ce_player = next(p for p in self.player_objects if p.player == player)
        if state.name == 'ChooseResources':
            ce_player.bonus_cards = [card for card in ce_player.bonus_cards if card.ID == option['BonusCard']]
            ce_player.hand = [c for c in ce_player.hand if c.ID in option['Cards']]
            for talent in option['Talents']:
                ce_player.talents.add_talent(talent, 1)
        elif state.name == 'PlayerTurn':
            new_states = []
            if option['Action'] == 'TalentHunt':
                talents, optional = ce_player.board.top_action()
                new_states = talents * [GameState('TakeTalent', player)]
                new_states += optional * [GameState('TakeTalentPayingCard', player)]
                # add states for possible triggers from other players to happen after turn end
            elif option['Action'] == 'ShowAds':
                money, optional = ce_player.board.mid_action()
                new_states = money * [GameState('EarnMoney', player)]
                new_states += optional * [GameState('EarnMoneyPayingTalent', player)]
                # add states for possible triggers from other players to happen after turn end
            elif option['Action'] == 'RecruitAttractions':
                cards, optional = ce_player.board.bot_action()
                new_states = cards * [GameState('DrawCard', player)]
                new_states += optional * [GameState('DrawCardPayingMoney', player)]
                # add states for possible triggers from other players to happen after turn end
            elif option['Action'] == 'PlayCard':
                card = option['Card']
                new_states = card.Cost * [GameState('PlayCardPayMoney', player)]
                new_states.append(GameState('PlayCardPayTalents', player))
                # add states for possible triggers from WHEN PLAYED effects
                new_states.append(GameState('PlayCardUpgradeChampion', player))
                # add states for possible triggers from other players to happen after turn end
            self.state_machine.add_states_to_next(new_states)
        elif state.name == 'TakeTalent':
            pass
        elif state.name == 'TakeTalentPayingCard':
            pass
        elif state.name == 'EarnMoney':
            pass
        elif state.name == 'EarnMoneyPayingTalent':
            pass
        elif state.name == 'DrawCard':
            pass
        elif state.name == 'DrawCardPayingMoney':
            pass
        elif state.name == 'PlayCardPayMoney':
            pass
        elif state.name == 'PlayCardPayTalents':
            pass
        elif state.name == 'PlayCardUpgradeChampion':
            pass
        else:
            raise InvalidStateException()

    def next_player_state(self, player, current_player, state):
        if state.name == 'ChooseResources':
            return CEChooseResources(player, current_player,
                                     self.deck, self.bonus_cards.number_of_cards(),
                                     self.objective_board, self.stage, self.player_objects)
        elif state.name == 'PlayerTurn':
            return CEPlayerTurn(player, current_player,
                                self.deck, self.bonus_cards.number_of_cards(),
                                self.objective_board, self.stage, self.player_objects)
        elif state.name == 'TakeTalent':
            return CETakeTalent(player, current_player,
                                self.deck, self.bonus_cards.number_of_cards(),
                                self.objective_board, self.stage, self.player_objects)
        elif state.name == 'TakeTalentPayingCard':
            return CETakeTalentPayingCard(player, current_player,
                                          self.deck, self.bonus_cards.number_of_cards(),
                                          self.objective_board, self.stage, self.player_objects)
        elif state.name == 'EarnMoney':
            return CEEarnMoney(player, current_player,
                               self.deck, self.bonus_cards.number_of_cards(),
                               self.objective_board, self.stage, self.player_objects)
        elif state.name == 'EarnMoneyPayingTalent':
            return CEEarnMoneyPayingTalent(player, current_player,
                                           self.deck, self.bonus_cards.number_of_cards(),
                                           self.objective_board, self.stage, self.player_objects)
        elif state.name == 'DrawCard':
            return CEDrawCard(player, current_player,
                              self.deck, self.bonus_cards.number_of_cards(),
                              self.objective_board, self.stage, self.player_objects)
        elif state.name == 'DrawCardPayingMoney':
            return CEDrawCardPayingMoney(player, current_player,
                                         self.deck, self.bonus_cards.number_of_cards(),
                                         self.objective_board, self.stage, self.player_objects)
        elif state.name == 'PlayCardPayMoney':
            return CEPlayCardPayMoney(player, current_player,
                                      self.deck, self.bonus_cards.number_of_cards(),
                                      self.objective_board, self.stage, self.player_objects)
        elif state.name == 'PlayCardPayTalents':
            return CEPlayCardPayTalents(player, current_player,
                                        self.deck, self.bonus_cards.number_of_cards(),
                                        self.objective_board, self.stage, self.player_objects)
        elif state.name == 'PlayCardUpgradeChampion':
            return CEPlayCardUpgradeChampion(player, current_player,
                                             self.deck, self.bonus_cards.number_of_cards(),
                                             self.objective_board, self.stage, self.player_objects)
        else:
            raise InvalidStateException()

    def readable_parameters(self):
        pass
