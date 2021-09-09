from enum import Enum
import string


class BoardSymbols(Enum):
    QUEEN_PIECE = "Q"
    EMPTY_SPACE = "."
    ATTACK_SPACE = "X"
    TAKEN_SPACE = "o"
    EM_DASH = "—"


def create_empty_board(n: int) -> list:
    """Create an empty matrix that represents a chessboard.
    n will define the length and width of the chessboard and the total number of queens."""
    board_length = board_width = n
    return [[BoardSymbols.EMPTY_SPACE] * board_length for _ in range(board_width)]


def display_board(board: list):
    """Print out the chessboard in an easy to understand way."""
    n = len(board)
    n_str_length = len(str(n))

    files = " " * (n_str_length + 3) + " ".join(f"{string.ascii_lowercase[:n]}")
    horizontal_line = " ".join(BoardSymbols.EM_DASH.value * n).rjust(
        n_str_length + n * 2 + 2
    )
    print(files, horizontal_line, sep="\n")

    for row_index, row in enumerate(board):
        ranks = f"{n - row_index} | ".rjust(n_str_length + 3)
        right_side_ranks = ranks[-3:] + ranks[:-3].strip()
        pieces = " ".join(
            "♛" if piece == BoardSymbols.QUEEN_PIECE else "." for piece in row
        )
        print(ranks + pieces + right_side_ranks)

    print(horizontal_line, files, sep="\n")


def get_positions(piece: BoardSymbols, board: list) -> list:
    """Get a list of positions on the chessboard that the piece of interest can be found."""
    return [
        [row_index, col_index]
        for row_index, row_value in enumerate(board)
        for col_index, col_value in enumerate(row_value)
        if col_value == piece
    ]


def place_queen(board: list) -> list:
    """Places a queen on a free and clear position without being attacked on the chess board."""
    board = mark_attacks(board)
    free_row, free_col = next(
        [row_index, col_index]
        for row_index, row_value in enumerate(board)
        for col_index, col_value in enumerate(row_value)
        if col_value == BoardSymbols.EMPTY_SPACE
    )

    board[free_row][free_col] = BoardSymbols.QUEEN_PIECE
    new_board = [[col for col in row] for row in board]
    board[free_row][free_col] = BoardSymbols.TAKEN_SPACE
    taken_board = [[col for col in row] for row in board]
    return new_board, taken_board


def can_place_queen(board: list) -> bool:
    """Checks if the chessboard has a valid spot for a queen."""
    return any(
        piece == BoardSymbols.EMPTY_SPACE
        for row in mark_attacks(board)
        for piece in row
    )


def mark_attacks(board: list) -> list:
    """Mark position on the board that can be attacked by a queen."""
    queen_positions = get_positions(BoardSymbols.QUEEN_PIECE, board)
    n = len(board)
    for queen_row, queen_col in queen_positions:
        board = [
            [
                BoardSymbols.ATTACK_SPACE
                if board[row][col] != BoardSymbols.QUEEN_PIECE
                and (
                    row == queen_row
                    or col == queen_col
                    or is_diagonal_to_queen([row, col], [queen_row, queen_col])
                )
                else board[row][col]
                for col in range(n)
            ]
            for row in range(n)
        ]
    return board


def is_diagonal_to_queen(board_position: list, queen_position: list) -> bool:
    """Checks if a position on the chessboard is diagonal to the queen piece."""
    row, col = board_position
    queen_row, queen_col = queen_position
    return abs(row - queen_row) == abs(col - queen_col)


def get_valid_boards(n: int) -> list:
    """Sets up the chessboard to start the process of finding valid board configurations."""
    if n == 0:
        # no chessboard, so no valid ways
        return []
    else:
        return get_valid_boards_helper(n, create_empty_board(n))


def get_valid_boards_helper(n_queens: int, board: list) -> list:
    """Gets a list of all valid n by n chessboard with n queens
    placed in such a way that no two queens attack each other."""
    if n_queens == 0:
        write_to_output_file(f"{get_positions(BoardSymbols.QUEEN_PIECE, board)}\n")
        return [board]
    elif can_place_queen(board):
        new_board, taken_board = place_queen(board)
        return get_valid_boards_helper(
            n_queens - 1, new_board
        ) + get_valid_boards_helper(n_queens, taken_board)

    return []


def display_example_board():
    board = create_empty_board(8)
    queen_positions = [[0, 7], [1, 3], [2, 0], [3, 2], [4, 5], [5, 1], [6, 6], [7, 4]]
    for x, y in queen_positions:
        board[x][y] = BoardSymbols.QUEEN_PIECE
    display_board(board)


def write_to_output_file(string: str):
    with open("output.txt", "a") as o:
        o.write(string)


if __name__ == "__main__":
    print("THE N QUEENS PUZZLE")
    display_example_board()

    print(
        "This program will solve the puzzle of placing n queens on "
        "an n by n chessboard such that no queens can attack each other!"
    )
    n = int(input("""Enter an integer n: """))
    print("""Getting all distinct solutions...\n""")

    write_to_output_file(f"{'='*20}\nSOLUTIONS FOR n={n}\n{'='*20}\n")
    valid_boards = get_valid_boards(n)
    write_to_output_file("\n\n\n\n")
    if not valid_boards:
        print("There are no possible solutions!")

    for board_index, board in enumerate(valid_boards):
        print(f"Solution {board_index+1}")
        display_board(board)
        print()

    print("Solutions have been saved to output.txt.")
