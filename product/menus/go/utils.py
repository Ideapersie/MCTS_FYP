from go import gotypes

COLS = 'ABCDEFGHJKLMNOPQRST'
Stone_To_Char = {
    None: ' . ',
    gotypes.Player.black: ' x ',
    gotypes.Player.white: ' o ',
}

def print_move(player, move):
    if move.is_pass:
        move_str = 'passes'
    elif move.is_resign:
        move_str = 'resigns'
    else:
        move_str = '%s%d' % (COLS[move.point.col - 1], move.point.row)
    
    print('%s %s' % (player, move_str))
    
def print_board(board):
    for row in range(board.num_rows, 0, -1):
        if row <= 9:
            bump = " "
        else:
            bump = ""
        line = []
        for col in range(1, board.num_cols + 1):
            stone = board.get(gotypes.Point(row=row, col=col))
            line.append(Stone_To_Char[stone])
        print('%s%d %s' % (bump, row, ''.join(line)))
    print(' ' + ' '.join(COLS[:board.num_cols]))
    