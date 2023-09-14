# import connect_ai_alpha_beta_pruning as caiab
import tictactoe_ai as tttai
import TicTacToe as ttt

SEARCH_DEPTH = 500
tictactoe = ttt.TicTactoe()

while tictactoe.has_winner() == 0 and not tictactoe.is_board_full():
    tictactoe.print_turn()
    # print('Make your move2 : ')
    # human_move2 = int(input())
    tictactoe.play_move(tttai.choose_move(tictactoe, SEARCH_DEPTH))
    # human_move_result2 = tictactoe.play_move(human_move2)
    tictactoe.print_board()
    print(tictactoe.has_winner())
    if tictactoe.has_winner() == 0:
        tictactoe.print_turn()
        human_move_result = False
        while human_move_result is False:
            print('Make your move: ')
            human_move = int(input())
            human_move_result = tictactoe.play_move(human_move)
        tictactoe.print_board()
        print(tictactoe.has_winner())