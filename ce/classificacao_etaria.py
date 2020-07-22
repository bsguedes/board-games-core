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
from ce.states.ce_pay_money import CEPayMoney
from ce.states.ce_play_card_upgrade_champion import CEPlayCardUpgradeChampion
from ce.states.ce_take_talent import CETakeTalent
from ce.states.ce_take_talent_paying_card import CETakeTalentPayingCard
from ce.states.ce_pay_cards import CEPayCards
from ce.states.ce_pay_talents import CEPayTalents
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
        self.channels: List[Channel] = loader.Channels
        shuffle(self.channels)

    def setup_game(self):
        self.player_objects = [CEPlayer(p, sample(c.Champions, 1)[0]) for p, c in zip(self.players, self.channels)]
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
                    turn = self.player_objects[(k + i) % n].player
                    self.state_machine.add_to_end(GameState('PlayerTurn', turn, {'Round': i, 'Turn': j}))
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
            ce_player.current_turn = state.args['Turn']
            ce_player.current_round = state.args['Round']
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
                playable_card = option['PlayableCard']
                ce_player.board.add_card_to_row(playable_card.ID, playable_card.Row)
                ce_player.hand.remove(next(c for c in ce_player.hand if c.ID == playable_card.ID))
                for talent in playable_card.TalentCost:
                    ce_player.talents.add_talent(talent, -1)
                new_states = playable_card.CashCost * [GameState('PayMoney', player)]
                # add states for possible triggers from WHEN PLAYED effects
                new_states.append(GameState('PlayCardUpgradeChampion', player))
                # add states for possible triggers from other players to happen after turn end
            self.state_machine.add_states_to_next(new_states)
        elif state.name == 'TakeTalent':
            if option['Action'] == 'Reroll':
                self.stage.reroll_all_dice()
                self.state_machine.add_to_next(GameState('TakeTalent', player))
            elif option['Action'] == 'TakeDie':
                ce_player.talents.add_talent(option['Talent'], 1)
                self.stage.take_die(option['Die'])
            elif option['Action'] == 'Cancel':
                self.state_machine.remove_states('TakeTalent', player)
        elif state.name == 'TakeTalentPayingCard':
            if option['Action'] != 'Cancel':
                if option['Action'] == 'Reroll':
                    self.stage.reroll_all_dice()
                    self.state_machine.add_to_next(GameState('TakeTalent', player))
                elif option['Action'] == 'TakeDiePayingCard':
                    ce_player.talents.add_talent(option['Talent'], 1)
                    self.stage.take_die(option['Die'])
                    ce_player.hand = [card for card in ce_player.hand if card.ID != option['Card']]
        elif state.name == 'EarnMoney':
            if option['Action'] == 'PlaceMoney':
                card = next(c for c in ce_player.board.cards_in_board() if c.ID == option['Card'])
                card.CurrentCash += 1
            elif option['Action'] == 'Cancel':
                self.state_machine.remove_states('EarnMoney', player)
        elif state.name == 'EarnMoneyPayingTalent':
            if option['Action'] == 'PlaceMoneyPayingTalent':
                card = next(c for c in ce_player.board.cards_in_board() if c.ID == option['Card'])
                card.CurrentCash += 1
                ce_player.talents.add_talent(option['Talent'], -1)
        elif state.name == 'DrawCard':
            if option['Action'] == 'BlindDraw':
                ce_player.hand.append(self.deck.draw_card())
            elif option['Action'] == 'DrawFromContracts':
                ce_player.hand.append(self.deck.take_from_contracts(option['Card']))
            elif option['Action'] == 'Cancel':
                self.state_machine.remove_states('DrawCard', player)
        elif state.name == 'DrawCardPayingMoney':
            if option['Action'] != 'Cancel':
                if option['Action'] == 'BlindDraw':
                    ce_player.hand.append(self.deck.draw_card())
                elif option['Action'] == 'DrawFromContracts':
                    ce_player.hand.append(self.deck.take_from_contracts(option['Card']))
                board_card = next(c for c in ce_player.board.cards_in_board() if c.ID == option['CashOrigin'])
                board_card.CurrentCash -= 1
        elif state.name == 'PayMoney':
            if option['Action'] == 'PayMoney':
                board_card = next(c for c in ce_player.board.cards_in_board() if c.ID == option['Card'])
                board_card.CurrentCash -= 1
        elif state.name == 'PlayCardUpgradeChampion':
            if option['Action'] == 'Upgrade':
                next_states = option['CashCost'] * [GameState('PayMoney', player)]
                next_states += [GameState('PayCards', player, option['CardCost'])]
                if any(n > 0 for t, n in option['TalentCost']):
                    next_states += [GameState('PayTalents', player, option['TalentCost'])]
                self.state_machine.add_states_to_next(next_states)
                ce_player.board.ChampionLevel += 1
        else:
            raise InvalidStateException(state.name)

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
        elif state.name == 'PayMoney':
            return CEPayMoney(player, current_player,
                              self.deck, self.bonus_cards.number_of_cards(),
                              self.objective_board, self.stage, self.player_objects)
        elif state.name == 'PlayCardUpgradeChampion':
            return CEPlayCardUpgradeChampion(player, current_player,
                                             self.deck, self.bonus_cards.number_of_cards(),
                                             self.objective_board, self.stage, self.player_objects)
        elif state.name == 'PayCards':
            return CEPayCards(player, current_player,
                              self.deck, self.bonus_cards.number_of_cards(),
                              self.objective_board, self.stage, self.player_objects, state.args)
        elif state.name == 'PayTalents':
            return CEPayTalents(player, current_player,
                                self.deck, self.bonus_cards.number_of_cards(),
                                self.objective_board, self.stage, self.player_objects, state.args)
        else:
            raise InvalidStateException(state.name)

    def readable_parameters(self):
        pass
