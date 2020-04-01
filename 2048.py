import random
from copy import deepcopy


class Board:
    """
    Holds the 4x4 board
    """
    def __init__(self):
        self.board = [[0]*4 for _ in range(4)]
        self.spawn_tile(value=2)
        self.spawn_tile(value=2)
        self.game_over = False
        self.score = 0

    def print_board(self):
        """
        Outputs the current state of the board
        :return:
        """
        for row in self.board:
            print(row)
        print()

    def spawn_tile(self, value=random.choices(population=[2, 4], weights=[.9, .1])[0]):
        """
        Spawns a new tile on the board
        :return:
        """
        empty_tiles = self.empty_tiles()
        row, col = random.choice(empty_tiles)
        self.board[row][col] = value

    def validate_move(self, direction):
        """
        Ensures that a move is possible
        :param direction:
        :return: boolean
        """

        # If the player picks a direction, and nothing happens, then that move isn't valid
        board_copy = deepcopy(self.board)
        self.make_move(direction=direction)
        if self.board == board_copy:
            return False

        return True

    def make_move(self, direction):
        """
        Moves all pieces in given direction
        :param direction: int (Up = 1, Right = 2, Down = 3, Left = 4)
        :return:
        """
        # Up
        if direction == 1:
            self.move_up()

        # Right
        if direction == 2:
            self.move_right()

        # Down
        if direction == 3:
            self.move_down()

        # Left
        if direction == 4:
            self.move_left()

    def move_up(self):
        """

        :return:
        """

        # Iterate through columns
        for j in range(4):
            merged = False

            # Current tile
            for i in range(1, 4):

                value = self.board[i][j]
                if not value:
                    continue

                # Next tile
                for k in range(i-1, -1, -1):
                    if not self.board[k][j]:
                        self.board[k][j] = value
                        self.board[k+1][j] = 0

                    # Hits a different value
                    elif self.board[k][j] != value:
                        break

                    # Merge (can only be done once per column)
                    elif not merged:
                        merged = True
                        self.board[k][j] = value*2
                        self.board[k+1][j] = 0
                        self.score += value*2
                        break

    def move_right(self):
        """

        :return:
        """
        for row in self.board:
            merged = False
            # Current tile
            for j in range(2, -1, -1):

                value = row[j]
                if not value:
                    continue

                # Next tile
                for k in range(j+1, 4):
                    if not row[k]:
                        row[k] = value
                        row[k-1] = 0

                    # Hit a different value
                    elif row[k] != value:
                        break

                    # Merge
                    elif not merged:
                        merged = True
                        row[k] = value*2
                        row[k-1] = 0
                        self.score += value*2
                        break

    def move_down(self):
        """

        :return:
        """
        # Iterate through columns
        for j in range(4):
            merged = False

            # Current tile
            for i in range(2, -1, -1):

                value = self.board[i][j]
                if not value:
                    continue

                # Next tile
                for k in range(i+1, 4):

                    # Blank tile
                    if not self.board[k][j]:
                        self.board[k][j] = value
                        self.board[k-1][j] = 0

                    # Hits another value
                    elif self.board[k][j] != value:
                        break

                    # Merge
                    elif not merged:
                        merged = True
                        self.board[k][j] = value*2
                        self.board[k-1][j] = 0
                        self.score += value*2
                        break

    def move_left(self):
        """

        :return:
        """
        for row in self.board:
            merged = False

            # Current Tile
            for j in range(1, 4):

                value = row[j]
                if not value:
                    continue

                # Next tile
                for k in range(j-1, -1, -1):
                    if not row[k]:
                        row[k] = value
                        row[k+1] = 0

                    # Hit a different value
                    elif row[k] != value:
                        break

                    # Merge
                    elif not merged:
                        merged = True
                        row[k] = value*2
                        row[k+1] = 0
                        self.score += value*2
                        break

    def empty_tiles(self):
        """
        Returns a list of all the empty tile locations
        :return: list of tuples
        """
        empty_tiles = []
        for i in range(4):
            for j in range(4):
                if not self.board[i][j]:
                    empty_tiles.append((i, j))

        return empty_tiles

    def check_game_state(self):
        """
        Checks if the game is over
        :return:
        """
        if self.empty_tiles():
            self.game_over = False
            return

        directions = [1, 2, 3, 4]
        board_copy = deepcopy(self.board)
        for direction in directions:
            if self.validate_move(direction=direction):
                self.game_over = False
                self.board = board_copy
                return

        self.game_over = True
        return


class Player:
    """
    Player for the game
    """
    def __init__(self):
        pass

    def choose_move(self):
        """
        Would you like to move up (1), right (2), down (3), or left (4)?
        :return:
        """
        direction_choice = int(input("Which direction would you like to move?"))

        return direction_choice


def create_board():
    return Board()


def create_player():
    return Player()


def play_game():
    """
    Controls the game loop
    :return:
    """
    board = create_board()
    player = create_player()

    print(f'STARTING GAME\n')
    while not board.game_over:
        board.print_board()

        move_choice = player.choose_move()
        while not board.validate_move(direction=move_choice):
            print(f'{move_choice} is an invalid choice. Choose again!')
            move_choice = player.choose_move()

        board.spawn_tile()
        board.check_game_state()

    board.print_board()
    print(f'GAME OVER. YOUR SCORE IS {board.score}')


def main():
    play_game()


if __name__ == '__main__':
    main()
