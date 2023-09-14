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


# This class encompasses the logic to play a game of connect.
class TicTactoe:
    def __init__(self, board_size=3):
        self.board_size = board_size
        self.player_turn = PLAYERS[ PLAYER_AI ]
        self.board = self.generate_board(board_size)

    # Reset the game with an empty board
    def reset(self):
        self.board = self.generate_board(self.board_size)

    def slot_contains(self, slot):
        x = TRANSFORM_DICT[ slot ][ 'x' ]
        y = TRANSFORM_DICT[ slot ][ 'y' ]
        return self.board[ x ][ y ]

    # Generate an empty board to begin on reset the game
    def generate_board(self, board_size):
        board = [ ]
        # board = [ [ _ , _ , _] , [ _ , _ , _ ], [ _ , _ , _ ] ]
        for _ in range(board_size):
            row = [ BOARD_EMPTY_SLOT ] * board_size
            board.append(row)
        return board

    # Print the board to console
    def print_board(self):
        result = ''
        for a in range(0, self.board_size):
            for b in range(0, self.board_size):
                result += self.board[ a ][ b ]
            result += '\n'
        print(result)

    # Print which player's turn it is
    def print_turn(self):
        if self.player_turn == PLAYERS[ PLAYER_HUMAN ]:
            print('It is Human to play')
        else:
            print('It is AI to play')

    # Determine if the game has a winner between the human and AI
    def has_winner(self):
        if self.has_a_row(PLAYER_HUMAN):
            return "Human won"
        elif self.has_a_row(PLAYER_AI):
            return "AI won"
        return 0

    # Get the score for the AI

    def get_score_for_ai(self):
        if self.has_a_row(PLAYER_HUMAN):
            return -10
        if self.has_a_row(PLAYER_AI):
            return 10
        return 0

    # Determine if a player has a row
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

    def has_a_diagonal(self, player, diagonal_number):
        for slot in diagonal_number:
            slot_value = self.slot_contains(slot)
            if not player == slot_value:
                return False
        return True


    # Determine if a player has a row given a starting point and offset
    # def has_row_of_x_from_point(self, player, row_count, x, y, offset_x, offset_y):
    #     total = 0
    #     for i in range(row_count):
    #         target_x = x + (i * offset_x)
    #         target_y = y + (i * offset_y)
    #         if self.is_within_bounds(target_x, target_y):
    #             if self.board[ target_x ][ target_y ] == player:
    #                 total += 1
    #     if total == row_count:
    #         return True
    #     return False

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

    # Execute a move for a player if there's space in the slot and choose the player based on whose turn it is
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
        return False
