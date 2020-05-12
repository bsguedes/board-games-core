from tictactoe.tictactoe import TicTacToe
from base_player import PlayerBase


def apply_option(game, player, x, y):
    possible_states = game.load_state_for_player(player).options
    option_code = next(c for c, o in possible_states.items() if o['X'] == x and o['Y'] == y)
    print(player.secret, option_code)
    valid = game.apply_option_on_current_state(player, option_code)
    print(valid)


parameters = {'X': 4, 'Y': 4, 'K': 3}
p1 = PlayerBase('p1')
p1.secret = 1
p2 = PlayerBase('p2')
p2.secret = 2
t = TicTacToe(parameters)
t.players = [p1, p2]
t.setup_game()
t.start_game()

apply_option(t, t.expecting_option_from, 2, 0)
apply_option(t, t.expecting_option_from, 0, 1)
apply_option(t, t.expecting_option_from, 1, 1)
apply_option(t, t.expecting_option_from, 1, 3)
apply_option(t, t.expecting_option_from, 0, 2)

print(t.load_state_for_player(p1).options)
print(t.load_state_for_player(p2).options)

for p, s in t.player_states.items():
    print(p, [d for _, d in s.items()][-1].as_dict())
