# Author: Joshua Arnett
# GitHub username: joshua-arnett
# Date: 06/05/24
# Description: Defines classes representing different chess pieces, all inheriting from a ChessPiece chess. Also defines a ChessVar class that represent an chess atomic chess game.

class ChessPiece:
    """Represents a chess piece."""

    def __init__(self, pos, color):
        self._pos = pos
        self._color = color
        self._piece = ""
        self._has_been_moved = False   # To keep track of pawns' available moves

    def get_piece(self):
        """Returns the picture of emoji of a chess piece."""
        return self._piece

    def set_piece(self, piece):
        """Set a piece equal to its picture or emoji."""
        self._piece = piece

    def get_pos(self):
        """Returns the position of a chess piece."""
        return self._pos

    def set_pos(self, new_pos):
        """Set the position of a chess piece. When called, self._has_been_moved is set to True."""
        self._pos = new_pos
        self._has_been_moved = True

    def get_color(self):
        """Returns the color of a chess piece."""
        return self._color

    def move_is_valid(self, move_to):
        """
        Returns True if a move is valid,
        by checking whether a tile is in the available_moves set returned by self.available_moves().
        """
        if move_to in self.available_moves():
            return True
        else:
            return False

    def available_moves(self):
        """Returns available moves based on type of chess piece (not checking for occupied tiles) within a set."""
        available_moves = set()
        current_position = self._pos
        columns_on_board = ["a", "b", "c", "d", "e", "f", "g", "h"]
        rows_on_board = ["1", "2", "3", "4", "5", "6", "7", "8"]

        # The ord() function assigns numbers (a key, if you will) to single-character strings.
        # We use this to index columns on the chess board.
        current_column_index = ord(current_position[0])

        current_column = current_position[0]
        current_row = int(current_position[1])

        # ---------------------- Helper Functions ----------------------- #
        def _set_temp_to_current():
            """Helper function for available diagonal moves."""
            return current_row, current_column_index

        def _add_diagonal_spaces():
            """Helper function for Queen and Bishop to add diagonal spaces."""
            # Top right diagonal
            temp_row, temp_column_index = _set_temp_to_current()
            while temp_column_index + 1 <= 104 and temp_row + 1 <= 8:
                available_moves.add(chr(temp_column_index + 1) + str(temp_row + 1))
                temp_column_index += 1
                temp_row += 1

            # Bottom right diagonal
            temp_row, temp_column_index = _set_temp_to_current()
            while temp_column_index + 1 <= 104 and temp_row - 1 >= 1:
                available_moves.add(chr(temp_column_index + 1) + str(temp_row - 1))
                temp_column_index += 1
                temp_row -= 1

            # Top left diagonal
            temp_row, temp_column_index = _set_temp_to_current()
            while temp_column_index - 1 >= 97 and temp_row + 1 <= 8:
                available_moves.add(chr(temp_column_index - 1) + str(temp_row + 1))
                temp_column_index -= 1
                temp_row += 1

            # Bottom left diagonal
            temp_row, temp_column_index = _set_temp_to_current()
            while temp_column_index - 1 >= 97 and temp_row - 1 >= 1:
                available_moves.add(chr(temp_column_index - 1) + str(temp_row - 1))
                temp_column_index -= 1
                temp_row -= 1

        def _add_vertical_and_horizontal_spaces():
            """Helper function for the Queen and Rook to add vertical and horizontal spaces."""
            # Sideways movement
            for column in columns_on_board:
                if current_column != column:
                    available_moves.add(column + str(current_row))

            # Up and down movement
            for row in rows_on_board:
                if str(current_row) != row:
                    available_moves.add(current_column + row)

        # ----------------- Adding available moves based on piece type ---------------- #

        if type(self) is Pawn:
            # Black and white pieces move in opposing directions
            pawn_direction = 1
            if self._color == "Black":
                pawn_direction = -1

            # Advancing
            if self._has_been_moved is False:
                available_moves.add(current_column + str(current_row + 2 * pawn_direction))
            available_moves.add(current_column + str(current_row + 1 * pawn_direction))

            # Capturing
            # The chr() function undoes the ord() function.
            if current_column == "a":
                available_moves.add(chr(current_column_index + 1) + str(current_row + 1 * pawn_direction))
            elif current_column == "h":
                available_moves.add(chr(current_column_index - 1) + str(current_row + 1 * pawn_direction))
            else:
                available_moves.add(chr(current_column_index + 1) + str(current_row + 1 * pawn_direction))
                available_moves.add(chr(current_column_index - 1) + str(current_row + 1 * pawn_direction))

        elif type(self) is Rook:
            _add_vertical_and_horizontal_spaces()

        elif type(self) is Knight:
            # 1st direction (forward)
            if current_row + 2 <= 8:
                if current_column_index + 1 <= 104:
                    available_moves.add(chr(current_column_index + 1) + str(current_row + 2))
                if current_column_index - 1 >= 97:
                    available_moves.add(chr(current_column_index - 1) + str(current_row + 2))

            # 2nd direction (backward)
            if current_row - 2 >= 1:
                if current_column_index + 1 <= 104:
                    available_moves.add(chr(current_column_index + 1) + str(current_row - 2))
                if current_column_index - 1 >= 97:
                    available_moves.add(chr(current_column_index - 1) + str(current_row - 2))

            # 3rd direction (left)
            if current_column_index - 2 >= 97:
                if current_row + 1 <= 8:
                    available_moves.add(chr(current_column_index - 2) + str(current_row + 1))
                if current_row - 1 >= 1:
                    available_moves.add(chr(current_column_index - 2) + str(current_row - 1))

            # 4th direction (right)
            if current_column_index + 2 <= 104:
                if current_row + 1 <= 8:
                    available_moves.add(chr(current_column_index + 2) + str(current_row + 1))
                if current_row - 1 >= 1:
                    available_moves.add(chr(current_column_index + 2) + str(current_row - 1))

        elif type(self) is Bishop:
            # Add diagonals
            _add_diagonal_spaces()

        elif type(self) is Queen:
            # Add diagonals, verticals, and horizontals
            _add_diagonal_spaces()
            _add_vertical_and_horizontal_spaces()

        elif type(self) is King:
            # Top three tiles above the king
            available_moves.add(chr(current_column_index - 1) + str(current_row + 1))
            available_moves.add(chr(current_column_index) + str(current_row + 1))
            available_moves.add(chr(current_column_index + 1) + str(current_row + 1))

            # Two tiles beside the king (left and right)
            available_moves.add(chr(current_column_index - 1) + str(current_row))
            available_moves.add(chr(current_column_index + 1) + str(current_row))

            # Bottom three tiles below king
            available_moves.add(chr(current_column_index - 1) + str(current_row - 1))
            available_moves.add(chr(current_column_index) + str(current_row - 1))
            available_moves.add(chr(current_column_index + 1) + str(current_row - 1))

        return available_moves


class Pawn(ChessPiece):
    """
    Represents a pawn.
    The '_has_been_moved' data member is to keep track of which pawns can move forward two tiles.
    The pawn color is to determine its available moves, since white and black move in opposite directions.
    """
    def __init__(self, pos, color):
        super().__init__(pos, color)
        self.create_piece()

    def create_piece(self):
        """Create the chess piece image that represents the Pawn."""
        if self._color == "White":
            self.set_piece("♟")
        elif self._color == "Black":
            self.set_piece("♙")


class Rook(ChessPiece):
    """Represents a rook."""
    def __init__(self, pos, color):
        super().__init__(pos, color)
        self.create_piece()

    def create_piece(self):
        """Create the chess piece image that represents the Rook."""
        if self._color == "White":
            self.set_piece("♜")
        elif self._color == "Black":
            self.set_piece("♖")


class Knight(ChessPiece):
    """Represents a knight."""
    def __init__(self, pos, color):
        super().__init__(pos, color)
        self.create_piece()

    def create_piece(self):
        """Create the chess piece image that represents the Knight."""
        if self._color == "White":
            self.set_piece("♞")
        elif self._color == "Black":
            self.set_piece("♘")


class Bishop(ChessPiece):
    """Represents a bishop."""
    def __init__(self, pos, color):
        super().__init__(pos, color)
        self.create_piece()

    def create_piece(self):
        """Create the chess piece image that represents the Bishop."""
        if self._color == "White":
            self.set_piece("♝")
        elif self._color == "Black":
            self.set_piece("♗")


class Queen(ChessPiece):
    """Represents a queen."""
    def __init__(self, pos, color):
        super().__init__(pos, color)
        self.create_piece()

    def create_piece(self):
        """Create the chess piece image that represents the Queen."""
        if self._color == "White":
            self.set_piece("♛")
        elif self._color == "Black":
            self.set_piece("♕")


class King(ChessPiece):
    """Represents a king."""
    def __init__(self, pos, color):
        super().__init__(pos, color)
        self.create_piece()

    def create_piece(self):
        """Create the chess piece image that represents the King."""
        if self._color == "White":
            self.set_piece("♚")
        elif self._color == "Black":
            self.set_piece("♔")


class ChessVar:
    """ChessVar class to represent chess game, played by two players. White always starts first."""

    def __init__(self):
        self._unfinished = "UNFINISHED"
        self._white_wins = "WHITE_WON"
        self._black_wins = "BLACK_WON"

        # Initialize board
        self._all_rows_dict = {"8": [" ", " ", " ", " ", " ", " ", " ", " "],
                               "7": [" ", " ", " ", " ", " ", " ", " ", " "],
                               "6": [" ", " ", " ", " ", " ", " ", " ", " "],
                               "5": [" ", " ", " ", " ", " ", " ", " ", " "],
                               "4": [" ", " ", " ", " ", " ", " ", " ", " "],
                               "3": [" ", " ", " ", " ", " ", " ", " ", " "],
                               "2": [" ", " ", " ", " ", " ", " ", " ", " "],
                               "1": [" ", " ", " ", " ", " ", " ", " ", " "]}

        self._pos_to_piece_dict = {}
        self._game_status = self._unfinished
        self._whose_turn = "Black"
        self.initialize_pieces()
        self.update_turn()
        self.print_board()
        self.print_whose_turn()

        while self._game_status == self._unfinished:
            move_from, move_to = self.request_user_input()
            while self.make_move(move_from, move_to) is False:
                move_from, move_to = self.request_user_input()

    def initialize_pieces(self):
        """Initializes pieces on the board."""

        set_of_pieces = set()

        # White pieces
        set_of_pieces.add(Pawn("a2", "White"))
        set_of_pieces.add(Pawn("b2", "White"))
        set_of_pieces.add(Pawn("c2", "White"))
        set_of_pieces.add(Pawn("d2", "White"))
        set_of_pieces.add(Pawn("e2", "White"))
        set_of_pieces.add(Pawn("f2", "White"))
        set_of_pieces.add(Pawn("g2", "White"))
        set_of_pieces.add(Pawn("h2", "White"))
        set_of_pieces.add(Rook("a1", "White"))
        set_of_pieces.add(Rook("h1", "White"))
        set_of_pieces.add(Knight("b1", "White"))
        set_of_pieces.add(Knight("g1", "White"))
        set_of_pieces.add(Bishop("c1", "White"))
        set_of_pieces.add(Bishop("f1", "White"))
        set_of_pieces.add(Queen("d1", "White"))
        set_of_pieces.add(King("e1", "White"))

        # Black pieces
        set_of_pieces.add(Pawn("h7", "Black"))
        set_of_pieces.add(Pawn("g7", "Black"))
        set_of_pieces.add(Pawn("f7", "Black"))
        set_of_pieces.add(Pawn("e7", "Black"))
        set_of_pieces.add(Pawn("d7", "Black"))
        set_of_pieces.add(Pawn("c7", "Black"))
        set_of_pieces.add(Pawn("b7", "Black"))
        set_of_pieces.add(Pawn("a7", "Black"))
        set_of_pieces.add(Rook("h8", "Black"))
        set_of_pieces.add(Rook("a8", "Black"))
        set_of_pieces.add(Knight("b8", "Black"))
        set_of_pieces.add(Knight("g8", "Black"))
        set_of_pieces.add(Bishop("f8", "Black"))
        set_of_pieces.add(Bishop("c8", "Black"))
        set_of_pieces.add(Queen("d8", "Black"))
        set_of_pieces.add(King("e8", "Black"))

        for piece in set_of_pieces:
            # Put each piece on the board and link their positions on the board to their respective ChessPiece objects
            self.put_piece_on_the_board(piece)
            self._pos_to_piece_dict[piece.get_pos()] = piece

    def request_user_input(self):
        """Asks the user what their desired moved is."""

        move_from = input("Move piece from: ")
        move_to = input("Move piece to: ")
        print()

        return move_from, move_to

    def clear_tile_on_board(self, tile_position):
        """Clears the current chess tile, given its position on the board."""

        # The ord() function assigns single-character strings to numbers.
        # We subtract 97 to make the keys for letters 'a' through 'h' equal 0-7.
        # This allows us to index through each list of rows to find the appropriate column.
        column_index_to_be_cleared = ord(tile_position[0]) - 97
        desired_row_to_be_cleared = tile_position[1]

        self._all_rows_dict[desired_row_to_be_cleared][column_index_to_be_cleared] = " "

    def put_piece_on_the_board(self, chess_piece):
        """Puts chess piece on the board."""

        # The ord() function assigns single-character strings to numbers.
        # We subtract 97 to make the keys for letters 'a' through 'h' equal 0-7.
        # This allows us to index through each list of rows to find the appropriate column.
        position = chess_piece.get_pos()
        desired_column = ord(position[0]) - 97
        desired_row = position[1]

        self._all_rows_dict[desired_row][desired_column] = chess_piece.get_piece()

    def make_move(self, move_from, move_to):
        """
        Move a chess piece from one tile to another.
        If the square being moved from does not contain a piece belonging to the player whose turn it is, or if the indicated move is not allowed, or if the game has already been won, then it returns False.
        Otherwise, it makes the indicated move, removes any captured (exploded) pieces from the board, updates the game state (unfinished to who wins) if necessary, updates whose turn it is, and returns True.
        Calls print_board() and update_turn() automatically when returning True.
        If either king is captured, it calls self.declare_winner().
        """

        home_tile = move_from.lower()
        destination_tile = move_to.lower()

        # ------------------------------------ Data Validation ---------------------------------------#

        if self.characters_are_invalid(home_tile, destination_tile):
            # If home or destination tile are invalid tiles, return False.
            print("Enter valid moves.")
            return False

        if self.out_of_bounds(home_tile) or self.out_of_bounds(destination_tile):
            # If the home or destination tile is out of bounds, return False.
            print("Move is out of bounds.")
            return False

        if home_tile == destination_tile:
            # If both position arguments are equal, the piece has not moved.
            print("You must move a piece.")
            return False

        if self._game_status != self._unfinished:
            # If the game has already ended, return False.
            print("Game has ended.")
            return False

        if self._pos_to_piece_dict[home_tile].get_color() != self._whose_turn:
            # If piece being moved does not belong to current player's color, return False.
            print("The piece you are trying to move is not yours.")
            return False

        if self._pos_to_piece_dict[home_tile].move_is_valid(destination_tile) is False:
            # If the destination tile is not a valid move based on the piece's position, return False.
            print("Your piece cannot make that move.")
            return False

        # The ord() function assigns single-character strings to numbers.
        # We subtract 97 to make the keys for letters 'a' through 'h' equal 0-7.
        # This allows us to index through each row to find the appropriate column.
        current_column = ord(home_tile[0]) - 97
        current_row = home_tile[1]
        current_tile = self._all_rows_dict[current_row][current_column]

        desired_column = ord(destination_tile[0]) - 97
        desired_row = destination_tile[1]
        desired_tile = self._all_rows_dict[desired_row][desired_column]

        if current_tile == " ":
            # If there is no piece on the current tile, return False.
            print("No piece to move on that tile.")
            return False

        if type(self._pos_to_piece_dict[home_tile]) is Pawn:
            # If the piece we are moving is a pawn

            if desired_tile == " " and home_tile[0] != destination_tile[0]:
                # The 0th index of the position arguments are the columns.
                # If the columns are not the same letter, the Pawn is capturing.
                # This is only allowed if the destination tile is occupied by a piece of the other color.
                print("Your pawn cannot capture an empty tile.")
                return False
            if desired_tile != " " and home_tile[0] == destination_tile[0]:
                # The 0th index of the position arguments are the columns.
                # If the columns are the same letter, the Pawn is advancing forward.
                # This is not allowed if the destination tile is occupied.
                print("Your piece cannot make that move.")
                return False

        if (type(self._pos_to_piece_dict[home_tile]) is not Knight and
                type(self._pos_to_piece_dict[home_tile]) is not Pawn):
            # The purpose of this if statement is to fix the issue of a piece
            # travelling to a vacant tile while another piece is in the way

            temp_column = current_column
            temp_row = int(current_row)

            if home_tile[0] == destination_tile[0]:
                # The 0th index of the position arguments are the columns. When equal, we are moving up or down.

                if current_row > desired_row:
                    # We increment the value of temp so that we are not analyzing the tile we're on
                    temp_row -= 1
                    while temp_row > int(desired_row) and self._all_rows_dict[str(temp_row)][temp_column] == " ":
                        # While the row we are at is higher than our destination row,
                        # we increment down and keep checking if the tile is empty
                        temp_row -= 1
                    if temp_row > int(desired_row):
                        # If  we are not at our destination tile yet after the while loop expires,
                        # there is a piece blocking the path to the destination tile.
                        print("Your piece cannot make that move.")
                        return False
                else:
                    # We increment the value of temp so that we are not analyzing the tile we're on
                    temp_row += 1
                    while temp_row < int(desired_row) and self._all_rows_dict[str(temp_row)][temp_column] == " ":
                        # While the row we are at is lower than our destination column,
                        # we increment up and keep checking if the tile is empty
                        temp_row += 1
                    if temp_row < int(desired_row):
                        # If the row is still lower after the while loop expires,
                        # there is a piece blocking the path to the destination tile.
                        print("Your piece cannot make that move.")
                        return False

            elif temp_row == int(desired_row):
                # If the current and destination tiles are on the same row

                if temp_column > desired_column:

                    # We increment the value of temp so that we are not analyzing the tile we're on
                    temp_column -= 1
                    while temp_column > desired_column and self._all_rows_dict[str(temp_row)][temp_column] == " ":
                        # While the column we are at is further right from our destination column,
                        # we increment left and keep checking if the tile is empty
                        temp_column -= 1
                    if temp_column > desired_column:
                        # If the column is still further right after the while loop expires,
                        # there is a piece blocking the path to the destination tile.
                        print("Your piece cannot make that move.")
                        return False
                else:
                    # We increment the value of temp so that we are not analyzing the tile we're on
                    temp_column += 1
                    while temp_column < desired_column and self._all_rows_dict[str(temp_row)][temp_column] == " ":
                        # While the column we are at is further left from our destination column,
                        # we increment right and keep checking if the tile is empty
                        temp_column += 1
                    if temp_column < desired_column:
                        # If the column is still further left after the while loop expires,
                        # there is a piece blocking the path to the destination tile.
                        print("Your piece cannot make that move.")
                        return False

            elif temp_column < desired_column and temp_row < int(desired_row):
                # Destination tile is in the top right diagonal

                # We increment the value of temp so that we are not analyzing the tile we're on
                temp_column += 1
                temp_row += 1
                while temp_column < desired_column and self._all_rows_dict[str(temp_row)][temp_column] == " ":
                    # While the column we are at is further left from our destination column,
                    # we increment right and up and keep checking if the tile is empty
                    temp_column += 1
                    temp_row += 1
                if temp_column < desired_column:
                    # If the column is still further left after the while loop expires,
                    # there is a piece blocking the path to the destination tile.
                    print("Your piece cannot make that move.")
                    return False

            elif temp_column < desired_column and temp_row > int(desired_row):
                # Destination tile is in the bottom right diagonal

                # We increment the value of temp so that we are not analyzing the tile we're on
                temp_column += 1
                temp_row -= 1
                while temp_column < desired_column and self._all_rows_dict[str(temp_row)][temp_column] == " ":
                    # While the column we are at is further left from our destination column,
                    # we increment right and down and keep checking if the tile is empty
                    temp_column += 1
                    temp_row -= 1
                if temp_column < desired_column:
                    # If the column is still further left after the while loop expires,
                    # there is a piece blocking the path to the destination tile.
                    print("Your piece cannot make that move.")
                    return False

            elif temp_column > desired_column and temp_row < int(desired_row):
                # Destination tile is in the top left diagonal

                # We increment the value of temp so that we are not analyzing the tile we're on
                temp_column -= 1
                temp_row += 1
                while temp_column > desired_column and self._all_rows_dict[str(temp_row)][temp_column] == " ":
                    # While the column we are at is further right from our destination column,
                    # we increment left and up and keep checking if the tile is empty
                    temp_column -= 1
                    temp_row += 1
                if temp_column > desired_column:
                    # If the column is still further right after the while loop expires,
                    # there is a piece blocking the path to the destination tile.
                    print("Your piece cannot make that move.")
                    return False

            elif temp_column > desired_column and temp_row > int(desired_row):
                # Destination tile is in the bottom left diagonal

                # We increment the value of temp so that we are not analyzing the tile we're on
                temp_column -= 1
                temp_row -= 1
                while temp_column > desired_column and self._all_rows_dict[str(temp_row)][temp_column] == " ":
                    # While the column we are at is further right from our destination column,
                    # we increment left and down and keep checking if the tile is empty
                    temp_column -= 1
                    temp_row -= 1
                if temp_column > desired_column:
                    # If the column is still further right after the while loop expires,
                    # there is a piece blocking the path to the destination tile.
                    print("Your piece cannot make that move.")
                    return False

        if desired_tile != " ":

            # --------------------------- CAPTURING --------------------------------- #

            if self._pos_to_piece_dict[destination_tile].get_color() == self._whose_turn:
                # Cannot capture a piece of the same color
                print("You cannot move to a tile that is being occupied by your own piece.")
                return False

            if type(self._pos_to_piece_dict[home_tile]) is King:
                # A king cannot capture in atomic chess
                print("Your king cannot make captures.")
                return False

            # If tests pass:
            # We explode the surroundings of the tile where the captured piece is by calling explode_surroundings

            if self.explode_surroundings(destination_tile) is False:
                # explode_surroundings returns False if two kings are blown up at once

                print("You cannot capture two kings at once.")
                return False
            else:
                # We delete the capturing piece from the pieces dictionary and clear the tile,
                # because all capturing pieces in atomic chess are suicidal.
                if home_tile in self._pos_to_piece_dict:
                    del self._pos_to_piece_dict[home_tile]
                    self.clear_tile_on_board(home_tile)

                self.print_board()

                # If the game status is still unfinished, the game goes on. Else, declare winner.
                if self._game_status == self._unfinished:
                    self.update_turn()
                    self.print_whose_turn()
                else:
                    self.declare_winner()

                return True

        # ------------------------- Moving without capturing ---------------------------- #

        # Move current piece to a different position in the dictionary
        piece = self._pos_to_piece_dict[home_tile]
        self._pos_to_piece_dict[destination_tile] = piece

        # Update piece's position attribute
        piece.set_pos(destination_tile)

        # Move chess piece image to destination tile
        piece_image = self._all_rows_dict[current_row][current_column]
        self._all_rows_dict[desired_row][desired_column] = piece_image

        # Clear tile we are moving from
        self.clear_tile_on_board(home_tile)

        self.update_turn()
        self.print_board()
        self.print_whose_turn()

        return True

    def print_whose_turn(self):
        """
        Prints whose turn it is.
        """
        print(f"{self._whose_turn}'s turn!\n")

    def update_turn(self):
        """
        Updates and prints whose turn it is.
        If current turn equals white, update to black. And vice versa.
        """
        if self._whose_turn == "White":
            self._whose_turn = "Black"
        else:
            self._whose_turn = "White"

    def get_game_state(self):
        """Returns the current game state."""
        return self._game_status

    def print_board(self):
        """Prints the board."""
        if self._whose_turn == "White":
            print("8 ", self._all_rows_dict["8"])
            print("7 ", self._all_rows_dict["7"])
            print("6 ", self._all_rows_dict["6"])
            print("5 ", self._all_rows_dict["5"])
            print("4 ", self._all_rows_dict["4"])
            print("3 ", self._all_rows_dict["3"])
            print("2 ", self._all_rows_dict["2"])
            print("1 ", self._all_rows_dict["1"])
            print("     A    B    C    D    E    F    G    H")
        elif self._whose_turn == "Black":
            # We print the rows backwards because they appear that way from black's perspective
            print("1 ", self._all_rows_dict["1"][::-1])
            print("2 ", self._all_rows_dict["2"][::-1])
            print("3 ", self._all_rows_dict["3"][::-1])
            print("4 ", self._all_rows_dict["4"][::-1])
            print("5 ", self._all_rows_dict["5"][::-1])
            print("6 ", self._all_rows_dict["6"][::-1])
            print("7 ", self._all_rows_dict["7"][::-1])
            print("8 ", self._all_rows_dict["8"][::-1])
            print("     H    G    F    E    D    C    B    A")
        print()

    def explode_surroundings(self, tile_pos):
        """
        Clears the capturing piece and all pieces surrounding it, except for pawns that are not directly attacked.
        Returns False if more than two kings are blown up at the same time.
        """

        pos_of_exploded_pieces = set()

        # The ord() function assigns single-character strings to numbers.
        # We subtract 97 to make the keys for letters 'a' through 'h' equal 0-7.
        # This allows us to index through each list of rows to find the appropriate column.
        column_index = ord(tile_pos[0]) - 97
        row = int(tile_pos[1])

        for row_num in range(-1, 2):
            # Going through the 3 x 3 block of tiles by iterating through each row
            # and column next to the captured piece.
            for num in range(-1, 2):

                # Create a tile position variable to simplify the code
                tile_position = chr(column_index + 97 + num) + str(row + row_num)

                # If certain tiles are out of bounds, we do not clear them.
                if self.out_of_bounds(tile_position) is False:

                    # If the tile is empty or if the tile is occupied by a pawn, we do not clear the tile.
                    if self._all_rows_dict[str(row + row_num)][column_index + num] != " " \
                            and type(self._pos_to_piece_dict[tile_position]) is not Pawn:

                        pos_of_exploded_pieces.add(tile_position)

        # If center tile position has not been added yet (due to it being a pawn), add it.
        if tile_pos not in pos_of_exploded_pieces:
            pos_of_exploded_pieces.add(tile_pos)

        # We count the number of kings exploded
        king_count = 0
        for tile_position in pos_of_exploded_pieces:
            if type(self._pos_to_piece_dict[tile_position]) is King:
                king_count += 1

        if king_count <= 1:
            # If number of kings is not more than 1, explode the tiles and return True.

            for tile_position in pos_of_exploded_pieces:
                self.clear_tile_on_board(tile_position)
                del self._pos_to_piece_dict[tile_position]

            if king_count == 1:
                # If one king is exploded, change game status so that the make_move() function can call declare_winner()
                self._game_status = self._whose_turn

            return True
        else:
            # Else, return False because we cannot explode two kings at the same time.
            return False

    def characters_are_invalid(self, str_1, str_2):
        """
        Returns False if the length of each string is 2, the first character is alphabetic, and the second is numeric.
        Returns True otherwise.
        """
        strings = [str_1, str_2]

        for string in strings:
            # Checking the length of each string
            if len(string) != 2:
                return True
            
            # If the characters are valid, do nothing
            elif string[0].isalpha() and string[1].isnumeric():
                pass
            
            # If the previous test did not pass, the string is invalid
            else:
                return True
        
        return False

    def out_of_bounds(self, tile_position):
        """Returns True if a tile's position is out of bounds, with respect to the chess board."""
        # The ord() function assigns single-character strings to numbers, with 'a' to 'h' being 97-104.
        # This allows us to index through each list of rows to find the appropriate column.
        if 97 <= ord(tile_position[0]) <= 104 and 1 <= int(tile_position[1]) <= 8:
            return False

        return True

    def is_game_over(self):
        """Returns True or False, depending on if either side has won yet."""
        if self._game_status == self._unfinished:
            return False
        else:
            return True

    def declare_winner(self):
        """Declares the winner."""
        winner = self._whose_turn
        if winner == "White":
            self._game_status = self._white_wins
        elif winner == "Black":
            self._game_status = self._black_wins

        print(f"{winner} wins!")
