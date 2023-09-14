import copy
import math
import random

# Set the min-max IDs, and pseudo infinity constants
MIN = -1
MAX = 1
INFINITY_POSITIVE = math.inf
INFINITY_NEGATIVE = -math.inf


# This class contains a move and the respective value earned for that move
class Move:

    def __init__(self, move=0, value=0):
        self.move = move
        self.value = value


# Choose a move given a game and a search depth
def choose_move(tictactoe, depth):
    print('Thinking...')
    move_result = False
    # Search for a move until a valid one is found
    while move_result is False:
        move_result = minmax(tictactoe, depth, MAX, 0, INFINITY_NEGATIVE, INFINITY_POSITIVE).move
    # print (move_result)
    return move_result


# Search using the minmax algorithm given a game, search depth, player's ID, and default move
def minmax(tictactoe, depth, min_or_max, move, alpha, beta):
    current_score = tictactoe.get_score_for_ai()
    current_is_board_full = tictactoe.is_board_full()
    # Return the default move if it doesn't make sense to search for one
    if current_score != 0 or current_is_board_full or depth == 0:
        return Move(move, current_score)

    best_score = INFINITY_NEGATIVE * min_or_max
    best_max_move = -1
    moves = [ n for n in range(9) ]
    random.shuffle(moves)
    # Try each move
    for slot in moves:
        neighbor = copy.deepcopy(tictactoe)
        move_outcome = neighbor.play_move(slot)

        if move_outcome:
            neighbor.print_board()
            # Recursively call minmax for the next state after playing a move
            best = minmax(neighbor, depth - 1, min_or_max * -1, slot, alpha, beta)
            # Update the best score and best move
            if (min_or_max == MAX and best.value > best_score) or (min_or_max == MIN and best.value < best_score):
                best_score = best.value
                best_max_move = best.move
                if best_score >= alpha:
                    alpha = best_score
                if best_score <= beta:
                    beta = best_score
            if alpha >= beta:
                break
    return Move(best_max_move, best_score)
