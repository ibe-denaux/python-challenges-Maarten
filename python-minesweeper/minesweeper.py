### 47 minesweeper

def board(input_board):
    # first get row and column count
    row_count = len(input_board)
    row_length = len(input_board[0])

    # check formal correctness: an error is raised when a formal demand is not met
    check_field_correctness(input_board, row_count, row_length)

    # make a new board with added bomb numbers
    output_board = create_output_board(input_board, row_count, row_length)
    for row in output_board:    # optional: print it
        print(row)
    return output_board


def check_field_correctness(input_board: list, row_count: int, row_length: int):
    # check different properties
    check_equal_column_length(input_board, row_length)
    check_borders(input_board, row_count, row_length)
    check_between_borders(input_board, row_count, row_length)


def check_equal_column_length(input_board: list, row_length: int):
    # check every row: is it of equal length as the first_row_length?
    for row in input_board:
        each_row_length = len(row)
        if each_row_length != row_length:
            raise ValueError("InputError: columns must be of equal length")


def check_borders(input_board: list, rows: int, row_length: int):
    # check '+' in the corners
    if input_board[0][0] != '+' or input_board[0][row_length - 1] != '+' \
            or input_board[rows - 1][0] != '+' or input_board[rows - 1][row_length - 1] != '+':
        raise ValueError("every corner of the board must contain '+'")


    # check '-' on first and last row
    for column in range(1, row_length - 1):
        if input_board[0][column] != '-' or input_board[rows - 1][column] != '-':
            raise ValueError("upper and lower row must contain only '-' between"
                             " the '+' at the first and last column")

    # check '|' on first and last column
    for row in range(1, rows-1):
        row_first_character = input_board[row][0]
        last_column = row_length - 1
        row_last_character = input_board[row][last_column]
        if row_first_character != '|' or row_last_character != '|':
            raise ValueError("first and last column must contain only '|' in between the '+'")


def check_between_borders(input_board: list, rows: int, row_length: int):
    # first_cell_to_check = input_board[1][1]
    # last cell to check = input_board[rows-2][columns-2]
    for row in range(1, rows-1):
        for column in range(1, row_length - 1):
            if input_board[row][column] not in (' ', '*'):
                raise ValueError("inside the borders only ' ' and '*' are allowed")


def create_output_board(input_board: list, rows: int, row_length: int) -> list:

    # make an empty list to fill and return with as the new board
    output_board = []

    # add first row to output_board
    first_row = input_board[0]
    output_board.append(first_row)

    # create rows between first and last row
    # loop through every cell of the board field inside the borders
    for row in range(1, rows-1):
        # for every loop, make an inside_row to fill and add to the output_board
        inside_row = ''

        # add first fixed column character '|'
        inside_row += input_board[row][0]

        # check the input_board fields for ' ' or '*', count bombs if necessary, add a suiting char to inside_row
        for column in range(1, row_length - 1):
            cell = input_board[row][column]
            if cell == ' ':
                number_of_bombs_around = calculate_number_of_bombs_around(input_board, row, column)
                if number_of_bombs_around > 0:
                    inside_row += str(number_of_bombs_around)
                else:
                    inside_row += ' '
            else:  # cell == '*'
                inside_row += '*'

        # add last column character
        inside_row += input_board[row][row_length - 1]

        # add the inside_row of this for-loop to output_board
        output_board.append(inside_row)

    # add last row to output_board
    last_row = input_board[rows-1]
    output_board.append(last_row)

    return output_board


def calculate_number_of_bombs_around(input_board: list, row: int, row_length: int) -> int:
    # you can count the borders without a worry: there are no '*' there
    # you can count the cell itself without a worry: no '*' there

    surrounding_bombs_count = 0

    # identify each surrounding cell and check for a bomb. If found, add 1 bomb to the count
    for surrounding_row in range(row-1, row+2):
        for surrounding_column in range(row_length - 1, row_length + 2):
            surrounding_cell = input_board[surrounding_row][surrounding_column]
            if surrounding_cell == '*':
                surrounding_bombs_count += 1

    return surrounding_bombs_count
