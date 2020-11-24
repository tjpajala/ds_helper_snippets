def move_column_inplace(df, col, pos):
    """
    Move column to position in df.
    :param df: Pandas DF.
    :param col: Column name.
    :param pos: Position as integer (0 is first)
    :return: Nothing, moves in-place.
    """
    col = df.pop(col)
    df.insert(pos, col.name, col)