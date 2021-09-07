import string

# Symbols on the chessboard
QUEEN_PIECE = "Q"
EMPTY_SPACE = "."
ATTACK_SPACE = "X"
TAKEN_SPACE = "o"
EM_DASH = "—"


def display_board(board: list) -> list:
    """Print out the chessboard in an easy to understand way."""
    n = len(board)
    print(" " * (len(str(n)) + 3) + " ".join(f"{string.ascii_lowercase[:n]}"))
    print(" ".join(EM_DASH * n).rjust(len(str(n)) + n * 2 + 2))
    print(
        "\n".join(
            f"{n - row_index} | ".rjust(len(str(n)) + 3)
            + " ".join("♛" if piece == QUEEN_PIECE else "." for piece in row)
            + f" | {n - row_index}"
            for row_index, row in enumerate(board)
        )
    )
    print(" ".join(EM_DASH * n).rjust(len(str(n)) + n * 2 + 2))
    print(" " * (len(str(n)) + 3) + " ".join(f"{string.ascii_lowercase[:n]}"))


def get_positions(piece: str, board: list) -> list:
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
        if col_value == EMPTY_SPACE
    )

    board[free_row][free_col] = QUEEN_PIECE
    new_board = [[col for col in row] for row in board]
    board[free_row][free_col] = TAKEN_SPACE
    taken_board = [[col for col in row] for row in board]
    return new_board, taken_board


def can_place_queen(board: list) -> bool:
    """Checks if the chessboard has a valid spot for a queen."""
    board = mark_attacks(board)
    valid_position = any(piece == EMPTY_SPACE for row in board for piece in row)
    return valid_position


def mark_attacks(board: list) -> list:
    """Mark position on the board that can be attacked by a queen."""
    queen_positions = get_positions(QUEEN_PIECE, board)
    n = len(board)
    for queen_row, queen_col in queen_positions:
        board = [
            [
                ATTACK_SPACE
                if board[row][col] != QUEEN_PIECE
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
    if abs(row - queen_row) == abs(col - queen_col):
        return True
    return False


def get_valid_boards(n: int) -> list:
    """Sets up the chessboard to start the process of finding valid board configurations."""
    if n == 0:
        # no chessboard, so no valid ways
        return []
    else:
        return get_valid_boards_helper(n, create_board(n))


def get_valid_boards_helper(n_queens: int, board: list) -> list:
    """Gets a list of all valid n by n chessboard with n queens 
    placed in such a way that no two queens attack each other."""
    if n_queens == 0:
        return [board]
    elif can_place_queen(board):
        new_board, taken_board = place_queen(board)
        return get_valid_boards_helper(
            n_queens - 1, new_board
        ) + get_valid_boards_helper(n_queens, taken_board)

    return []


def create_board(n: int) -> list:
    """Create an empty matrix that represents a chessboard.
    n will define the length and width of the chessboard and the total number of queens."""
    board_length = board_width = n
    empty_board = [[EMPTY_SPACE] * board_length for _ in range(board_width)]
    return empty_board


if __name__ == "__main__":
    print(
        "This program will solve the puzzle of placing n queens on "
        "an n by n chessboard such that no queens can attack each other!"
    )
    n = int(input("""Enter an integer n: """))
    print("""Getting all distinct solutions...\n""")

    valid_boards = get_valid_boards(n)
    if not valid_boards:
        print("There are no possible solutions!")

    for board_index, board in enumerate(valid_boards):
        print(f"Solution {board_index+1}")
        display_board(board)
        print()
