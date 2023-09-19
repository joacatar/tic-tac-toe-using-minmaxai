#Authorship:Joao Tarira working with  Amarra Houraney & Matthew Bush 

from prettytable import PrettyTable
import copy
import math
import random
import time


SEARCH_DEPTH = 10

# Set the min-max IDs, and pseudo infinity constants
MIN = -1
MAX = 1
INFINITY_POSITIVE = math.inf
INFINITY_NEGATIVE = -math.inf


# Symbols to represent human or AI players
PLAYER_HUMAN = 'X'
PLAYER_AI = 'O'
BOARD_EMPTY_SLOT = '_'
WINNING_SEQUENCE_COUNT = 3
TRANSFORM_DICT = {
    0: { "x": 0, "y": 0 },
    1: { "x": 0, "y": 1 },
    2: { "x": 0, "y": 2 },
    3: { "x": 1, "y": 0 },
    4: { "x": 1, "y": 1 },
    5: { "x": 1, "y": 2 },
    6: { "x": 2, "y": 0 },
    7: { "x": 2, "y": 1 },
    8: { "x": 2, "y": 2 }
}
DIAGONAL1 = [0, 4, 8]
DIAGONAL2 = [2, 4, 6]

# Tuple encoding human player as -1, and AI player as 1
PLAYERS = {
    PLAYER_HUMAN: -1,
    PLAYER_AI: 1 }


# This class encompasses the logic to play a game of tictactoe.
class TicTactoe:
    def __init__(self, board_size=3):
        self.board_size = board_size
        self.player_turn = PLAYERS[ PLAYER_AI ]
        self.board = self.generate_board(board_size)

    # Reset the game with an empty board
    def reset(self):
        self.board = self.generate_board(self.board_size)

    # determines the value of the slot just by inputting slot value
    # and translate it to the coordinate system of the board
    def slot_contains(self, slot):
        x = TRANSFORM_DICT[ slot ][ 'x' ]
        y = TRANSFORM_DICT[ slot ][ 'y' ]
        return self.board[ x ][ y ]

    # Generate an empty board to begin on reset the game
    def generate_board(self, board_size):
        board = [ ]
        # board = [ [ _ , _ , _] , [ _ , _ , _ ], [ _ , _ , _ ] ]
        sample_board = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        sample_tutorial = PrettyTable()
        for row in sample_board:
            sample_tutorial.add_row(row)
        sample_tutorial.header = False
        print(sample_tutorial)
        for _ in range(board_size):
            row = [BOARD_EMPTY_SLOT] * board_size
            board.append(row)

        return board

    # Print the board to console
    def print_board(self):
        table_to_print = PrettyTable()
        for row in self.board:
            table_to_print.add_row(row)
        table_to_print.header = False
        print(table_to_print)

    # Print which player's turn it is
    def print_turn(self):
        if self.player_turn == PLAYERS[ PLAYER_HUMAN ]:
            print('It is Human to play')
        else:
            print('It is AI to play')

    # Determine if the game has a winner between the human and AI
    def has_winner(self):
        if self.has_a_row(PLAYER_HUMAN):
            return "🎉 Victory! You've triumphed over AI! 💪🏆"
        elif self.has_a_row(PLAYER_AI):
            return "😱 Oh no! AI's got the skills! AI wins! 🤖🏆"
        return 0

    # Get the score for the AI
    def get_score_for_ai(self):
        if self.has_a_row(PLAYER_HUMAN):
            return -10
        if self.has_a_row(PLAYER_AI):
            return 10
        return 0

    # Determine if a player has a row or column or a diagonal
    def has_a_row(self, player):
        if self.has_a_row_or_column(player, 3, 1, 1):  # Horizontal row
            return True
        elif self.has_a_row_or_column(player, 1, 7, 3):  # Vertical row
            return True
        elif self.has_a_diagonal(player, DIAGONAL1):  # Diagonal row
            return True
        elif self.has_a_diagonal(player, DIAGONAL2):  # Diagonal row
            return True
        return False

    # determines if player has a row or column depending on the a,b,c values
    # Determine if a player has a row or column depending on the 'a', 'b', and 'c' parameters.
    # For rows, 'a' represents the starting slot, 'b' represents the difference between slots in a row,
    # and 'c' represents the step size to iterate through the row slots (0, 1, 2).
    # For columns, 'a' represents the starting slot, 'b' represents the difference between slots in a column,
    # and 'c' represents the step size to iterate through the column slots (0, 3, 6).
    def has_a_row_or_column(self, player, a, b, c):
        for i in range(3):
            total = 0
            for j in (range(a * i, (i + b) * a, c)):
                slot_value = self.slot_contains(j)
                if player == slot_value:
                    total += 1
                else:
                    j = (i + b) * a
                # print(f"{j} : {player}")
            # print(total)
            if total == WINNING_SEQUENCE_COUNT:
                return True
        return False

    # determines if player has a diagonal 0,4,8 or 2,4,6 from dictionary
    def has_a_diagonal(self, player, diagonal_number):
        for slot in diagonal_number:
            slot_value = self.slot_contains(slot)
            if not player == slot_value:
                return False
        return True

    # Determine if a specific x,y pair is within bounds of the board
    def is_within_bounds(self, x, y):
        if 0 <= x < self.board_size and 0 <= y < self.board_size:
            return True
        return False

    # Determine if the entire board is filled with disks
    def is_board_full(self):
        for x in range(self.board_size):
            for y in range(self.board_size):
                if BOARD_EMPTY_SLOT in self.board[x][y]:
                    return False
        return True

    # Determine if a slot is full
    def is_slot_full(self, slot_number):
        slot_value = self.slot_contains(slot_number)
        if BOARD_EMPTY_SLOT in slot_value:
            return False
        return True

    # Determine if a slot number is empty
    def is_slot_empty(self, slot_number):
        count = 0
        for i in range(self.board_size):
            if self.board[slot_number][i] == BOARD_EMPTY_SLOT:
                count += 1
        if count == self.board_size:
            return True
        return False

    # Execute a move for a player
    def execute_move(self, player, slot_number):
        x = TRANSFORM_DICT[slot_number]['x']
        y = TRANSFORM_DICT[slot_number]['y']
        if not self.is_slot_full(slot_number):
            self.board[x][y] = player

    # Execute a move for a player if there's space in the slot and choose the player based on
    # whose turn it is also checks if the move is within acceptable range of 0 to 8 if not it
    # prints that it is not valid and returns false
    def play_move(self, slot):
        if 0 <= slot <= 8:
            if not self.is_slot_full(slot):
                if self.player_turn == PLAYERS[PLAYER_AI]:
                    self.execute_move(PLAYER_AI, slot)
                else:
                    self.execute_move(PLAYER_HUMAN, slot)
                self.player_turn *= -1
                return True
            return False
        print("Please enter a valid move (0-8)")
        return False


# This class contains a move and the respective value earned for that move
class Move:
    def __init__(self, move=0, value=0):
        self.move = move
        self.value = value


# Choose a move given a game and a search depth
def choose_move(tictactoe_board, depth):
    print("🤖 Hold on, AI is pondering its next move... 🤔")
    move_result = False
    # Search for a move until a valid one is found
    while move_result is False:
        move_result = minmax(tictactoe_board, depth, MAX, 0).move
    print(f"🎉 Bam! AI has made its move to {move_result}! 🤖 Let's see what it's got! 💥")
    return move_result


# Search using the minmax algorithm given a game, search depth, player's ID, and default move
def minmax(tictactoe_board, depth, min_or_max, move):
    current_score = tictactoe_board.get_score_for_ai()
    current_is_board_full = tictactoe_board.is_board_full()
    # Return the default move if it doesn't make sense to search for one
    if current_score != 0 or current_is_board_full or depth == 0:
        return Move(move, current_score)

    best_score = INFINITY_NEGATIVE * min_or_max
    best_max_move = -1
    # Get possible moves given the board size
    moves = [n for n in range(9)]
    # To avoid repetitive outcomes when using the same depth over and over, we shuffle the list of possible moves.
    # This ensures that the AI explores different move sequences and adds an element of unpredictability to its choices.
    # By shuffling the moves, we prevent the AI from consistently making the same decisions when multiple moves yield the same score.
    random.shuffle(moves)
    for slot in moves:
        neighbor = copy.deepcopy(tictactoe_board)
        move_outcome = neighbor.play_move(slot)
        if move_outcome:
            # Recursively call minmax for the next state after playing a move
            best = minmax(neighbor, depth - 1, min_or_max * -1, slot)
            # Update the best score and best move
            if (min_or_max == MAX and best.value > best_score) or (min_or_max == MIN and best.value < best_score):
                best_score = best.value
                best_max_move = best.move
    return Move(best_max_move, best_score)


def choose_move_ab(tictactoe_board, depth):
    print("🤖 Hold on, AI is pondering its next move... 🤔")
    move_result = False
    # Search for a move until a valid one is found
    while move_result is False:
        move_result = minmax_ab(tictactoe_board, depth, MAX, 0, INFINITY_NEGATIVE, INFINITY_POSITIVE).move
    # print (move_result)
    print(f"🎉 Bam! AI has made its move to {move_result}! 🤖 Let's see what it's got! 💥")
    return move_result


# Search using the minmax algorithm given a game, search depth, player's ID, and default move
def minmax_ab(tictactoe_board, depth, min_or_max, move, alpha, beta):
    current_score = tictactoe_board.get_score_for_ai()
    current_is_board_full = tictactoe_board.is_board_full()
    # Return the default move if it doesn't make sense to search for one
    if current_score != 0 or current_is_board_full or depth == 0:
        return Move(move, current_score)

    best_score = INFINITY_NEGATIVE * min_or_max
    best_max_move = -1
    moves = [n for n in range(9)]
    # moves = [ 0, 1, 2 .... 8]
    # To avoid repetitive outcomes when using the same depth over and over, we shuffle the list of possible moves.
    # This ensures that the AI explores different move sequences and adds an element of unpredictability to its choices.
    # By shuffling the moves, we prevent the AI from consistently making the same decisions when multiple moves yield the same score.
    random.shuffle(moves)
    # moves = [ 1,6,3, ....]
    # Try each move
    for slot in moves:
        neighbor = copy.deepcopy(tictactoe_board)
        move_outcome = neighbor.play_move(slot)

        if move_outcome:
            # Recursively call minmax for the next state after playing a move
            best = minmax_ab(neighbor, depth - 1, min_or_max * -1, slot, alpha, beta)
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


def tic_tac_toe():
    while tictactoe.has_winner() == 0 and not tictactoe.is_board_full():
        tictactoe.print_turn()
        # Command to use minimax algorithm
        tictactoe.play_move(choose_move(tictactoe, SEARCH_DEPTH))
        # Command to use minimax algorithm with alpha beta
        # tictactoe.play_move(choose_move_ab(tictactoe, SEARCH_DEPTH))
        tictactoe.print_board()
        if tictactoe.has_winner() == 0 and not tictactoe.is_board_full():
            tictactoe.print_turn()
            human_move_result = False
            while human_move_result is False:
                try:
                    human_move = int(input("X's turn! Pick your move (0-8) and let's win this!🏆✨ "))
                except ValueError:
                    human_move = 60
                    # print("Please enter a valid move (0-8)")
                human_move_result = tictactoe.play_move(human_move)
            tictactoe.print_board()
        time.sleep(1)
    if tictactoe.has_winner() == 0:
        print("It is a draw!")
    else:
        print(tictactoe.has_winner())


def greeting():
    print("Welcome to Tic Tac Toe Showdown! 🎮 Challenge our AI opponents in a battle of wits.\n "
          "Will you outsmart the classic Minimax AI or take on the cunning Minimax AI with Alpha-Beta pruning?\n "
          "It's a test of strategy and skill. Play your moves wisely and aim for victory.\n "
          "🏆 When you're ready to face the challenge, just say 'Yes' to another round.\n Good luck, "
          "and let the games begin! 🚀🤖💥")


greeting()
tictactoe = TicTactoe()
game_continue = True
while game_continue:
    tic_tac_toe()
    user_input = input("Would you like to play another game? Enter y or n: ")
    if user_input.lower() == 'n':
        game_continue = False
        print("🚀🚀Thanks for using our up rate as 5 stars⭐⭐⭐⭐⭐")
    else:
        tictactoe.reset()
        print("🚀🚀Good luck against AI 🤯🤯")

