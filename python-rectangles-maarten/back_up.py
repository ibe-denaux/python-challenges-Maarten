def count(lines=[]):
    if type(lines) is not list:     # passes the count("")-test
        return 0
    elif len(lines) == 0:           # passes the count()-test
        return 0
    else:
        return count_squares(lines)


def count_squares(lines):
    rectangle_count = 0
    rows = len(lines)
    row_length = len(lines[0])

    for row in range(rows):
        for column in range(row_length):
            cell = lines[row][column]
            if cell == '+':

                check_top_line(lines, row, column)
                # start from top_row: how many times do we have to depart from this '+'?
                # Count + on top_row to the right of this '+'
                plus_indexes_top_row = indexes_plus_on_top_row(lines, row, column)
                # keep track of extra '+' that you have already checked in the following while loop.
                # Start with no checked '+'
                checked_plus_indexes_top_row = []

                while len(plus_indexes_top_row) > 0:
                    next_plus_index_top_row = plus_indexes_top_row.pop(0)   # track which to add to checked '+' after the check

                    # start check: look for next '+' on top line. The index of that '+' becomes index right column
                    # return -1 if there is no correct line (---) between (+---+)
                    right_column_index = top_line_check(lines, row, column, checked_plus_indexes_top_row)  #
                    if right_column_index != -1:
                        # count + on right column
                        plus_indexes_right_column = indexes_plus_on_right_column(lines, row, right_column_index)
                        checked_plus_indexes_right_column = []

                        while len(plus_indexes_right_column) > 0:
                            next_plus_index_right_column = plus_indexes_right_column.pop(0)

                            # check
                            bottom_row_index = right_line_check(lines, row, right_column_index,
                                                                checked_plus_indexes_right_column)
                            if bottom_row_index != -1:
                                # count + on bottom row
                                plus_indexes_bottom_row = indexes_plus_on_bottom_row(lines, bottom_row_index,
                                                                                     right_column_index)
                                checked_plus_indexes_bottom_row = []

                                while len(plus_indexes_bottom_row) > 0:
                                    next_plus_index_bottom_row = plus_indexes_bottom_row.pop(0)

                                    # check
                                    left_column_index = bottom_line_check(lines, bottom_row_index, right_column_index,
                                                                          checked_plus_indexes_bottom_row)

                                    if left_column_index != -1:
                                        # count + on left column
                                        plus_indexes_left_column = indexes_plus_on_left_column(lines, bottom_row_index,
                                                                                               left_column_index)
                                        checked_plus_indexes_left_column = []

                                        while len(plus_indexes_left_column) > 0:
                                            next_plus_index_left_column = plus_indexes_left_column.pop(0)

                                            # check
                                            top_row_index = left_line_check(lines, bottom_row_index, left_column_index,
                                                                            checked_plus_indexes_left_column)
                                            if top_row_index != -1:

                                                if home_base_check(top_row_index, left_column_index, row, column):
                                                    rectangle_count += 1
                                            checked_plus_indexes_left_column.append(next_plus_index_left_column)

                                    checked_plus_indexes_bottom_row.append(next_plus_index_bottom_row)

                            checked_plus_indexes_right_column.append(next_plus_index_right_column)

                    checked_plus_indexes_top_row.append(next_plus_index_top_row)

    print(rectangle_count)
    return rectangle_count


def check_top_line(lines, row, column):



def indexes_plus_on_top_row(lines, row_index_plus, column_index_plus):
    columns = len(lines[0])
    plus_indexes = []

    for column in range(column_index_plus + 1, columns):
        cell_to_check = lines[row_index_plus][column]
        if cell_to_check == '+':
            plus_indexes.append(column)
        elif cell_to_check == '-':
            continue
        else:
            return plus_indexes
    return plus_indexes


def indexes_plus_on_bottom_row(lines, bottom_row_index, right_column_index):
    plus_indexes = []

    for column in range(right_column_index - 1, -1, -1):  # add another -1
        cell_to_check = lines[bottom_row_index][column]
        if cell_to_check == '+':
            plus_indexes.append(column)
        elif cell_to_check == '-':
            continue
        else:
            return plus_indexes
    return plus_indexes


def indexes_plus_on_right_column(lines, row_start, right_column_index):
    rows = len(lines)
    plus_indexes = []

    for row in range(row_start + 1, rows):
        cell_to_check = lines[row][right_column_index]
        if cell_to_check == '+':
            plus_indexes.append(row)
        elif cell_to_check == '|':
            continue
        else:
            return plus_indexes

    return plus_indexes


def indexes_plus_on_left_column(lines, bottom_row_index, left_column_index):
    plus_indexes = []

    for row in range(bottom_row_index - 1, -1, -1):
        cell_to_check = lines[row][left_column_index]
        if cell_to_check == '+':
            plus_indexes.append(row)
        elif cell_to_check == '|':
            continue
        else:
            return plus_indexes
    return plus_indexes


def top_line_check(lines, row_index: int, column_index: int, checked_plus_indexes_top_row) -> int:
    for column in range(column_index + 1, len(lines[0])):
        cell_to_check = lines[row_index][column]
        if cell_to_check == '-':
            continue
        elif cell_to_check == '+':
            if column not in checked_plus_indexes_top_row:
                return column
        else:
            return -1
    return -1  # in case there are only '-'


def right_line_check(lines, row_index, new_column_index, checked_plus_indexes_right_column):
    for row in range(row_index + 1, len(lines)):
        cell_to_check = lines[row][new_column_index]
        if cell_to_check == '|':
            continue
        elif cell_to_check == '+':
            if row not in checked_plus_indexes_right_column:
                return row
        else:
            return -1
    return -1  # case only '|'


def bottom_line_check(lines, row_index, column_index, checked_plus_indexes_bottom_row):
    for column in range(column_index - 1, -1, -1):
        cell_to_check = lines[row_index][column]
        if cell_to_check == '-':
            continue
        elif cell_to_check == '+':
            if column not in checked_plus_indexes_bottom_row:
                return column
        else:
            return -1
    return -1


def left_line_check(lines, new_row_index, next_column_index, checked_plus_indexes_left_column):
    for row in range(new_row_index - 1, -1, -1):
        cell_to_check = lines[row][next_column_index]
        if cell_to_check == '|':
            continue
        elif cell_to_check == '+':
            if row not in checked_plus_indexes_left_column:
                return row
        else:
            return -1
    return -1


def home_base_check(last_row, next_column, original_row, original_column):
    if last_row == original_row and next_column == original_column:
        return True
    return False


# count(["  +-+",     # 2
#        "  | |",
#        "+-+-+",
#        "| |  ",
#        "+-+  "
#                  ])

# count(["  +-+",             # 5
#        "  | |",
#        "+-+-+",
#        "| | |",
#        "+-+-+" ])

# count(["  +-+",     # start several times from first + on a row  (count + on a row to determine how many times: 3+? start 2 times from first - work with column indexes in a list)
#        "  | |",     # 5
#        "+-+-+",
#        "| | |",
#        "+-+-+"])

# count(["  +-+",     # 1
#        "    |",
#        "+-+-+",
#        "| | -",
#        "+-+-+"
#                  ])

# count(["+------+----+",         # 3
#                  "|      |    |",
#                  "+---+--+    |",
#                  "|   |       |",
#                  "+---+-------+"
#                  ])

count(["+------+----+",  # 2
       "|      |    |",
       "+------+    |",
       "|   |       |",
       "+---+-------+"
       ])

# count(["+------+----+",    # only count 2 up to now instead of 3. Also on the bottom line: check for multiple plusses !
#        "|      |    |",
#        "+---+--+    |",
#        "|   |       |",
#        "+---+-------+"])
#
# count(["+------+----+",
#        "|      |    |",
#        "+------+    |",
#        "|   |       |",
#        "+---+-------+" ])
