from reversi.core.board import Player, Piece


REP_TO_PIECE = {
    'W': Player.ONE,
    'B': Player.TWO,
    ' ': None,
}

def construct_pieces(board_rep):
    rows = board_rep.split('\n')
    assert len(rows) == len(rows[0])
    pieces = []
    for row in rows:
        pieces_row = []
        for piece in row:
            if piece == ' ':
                pieces_row.append(None)
            else:
                pieces_row.append(Piece(REP_TO_PIECE[piece]))
        pieces.append(pieces_row)
    return pieces

    # return [
    #     [Piece(colour=REP_TO_PIECE[piece]) for piece in row if piece != ' ' else None]
    #     for row in rows
    # ]
    #  the above is invalid syntax.. SMH!
