import pandas as pd
from IPython.core.display import display


def move_column_inplace(df: pd.DataFrame, col: str, pos: int) -> None:
    """
    Move column to position in df.
    :param df: Pandas DF.
    :param col: Column name.
    :param pos: Position as integer (0 is first)
    :return: Nothing, moves in-place.
    """
    col = df.pop(col)
    df.insert(pos, col.name, col)

def print_top_n_per_group(df: pd.DataFrame, groupby_var: str, var: str, top_n: int = 10) -> None:
    """
    Display `top_n` most common observations of variable `var` per group in `groupby_var`.
    :param df: Pandas DataFrame
    :param groupby_var: String variable name to group by.
    :param var: String variable name of the variable of interest.
    :param top_n: Intger of number of top elements per group.
    :return: Nothing
    """
    for g in df[groupby_var].unique():
        print("\nTOP {} {}s for {}".format(top_n, var, g))
        d = df.loc[df.target_region == g,[groupby_var,var]].groupby([var]).size().reset_index()
        d.columns=[var,"count"]
        if d["count"].max()==1:
            print("All {}s in {} appear only once!".format(var, g))
            continue
        with pd.option_context('max_colwidth',0, "display.width",1000):
            display(d.sort_values("count",ascending=False).head(top_n))