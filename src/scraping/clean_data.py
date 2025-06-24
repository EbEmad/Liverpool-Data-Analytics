import pandas as pd
def flatten_columns(df):
    """flattens multi-level column headers and clean names."
        Replace spaces with underscroes and removes 'Unamed' levels
    """

    if isinstance(df.columns,pd.MultiIndex):
        df.columns=[
            '_'.join([str(lv).strip().replace(' ','_') for lv in col if 'Unnamed' not in str(lv)]).strip('_')
            for col in df.columns
        ]

    else:
        df.columns=[
            str(col).strip().replace(' ','_') for col in df.columns
        ]
    
    # Lowercase all column names
    df.columns=[col.lower() for col in df.columns]
    return df

def clean_table(club,table):
    """
        Cleans the Championship stats table:
        - Drops unnecessary columns if they exist (case-insensitive, space-insenstive)
        - Remove rows like 'Squad Total'm'Opponent Total',or 'Player' header rows
    """

    # normalized column names for reliable matching
    normalized_columns={col.lower().strip().replace(' ','_'): col for col in table.columns}
    liverpool_columns_to_drop_raw=["matches", "match_report", "notes"]
    championship_columns_to_drop_raw = ["rk", "born", "matches"]
    if club=='Liverpool':
        if 'mp' in table.columns:
            table.rename(columns={'mp':'playing_time_mp'},inplace=True)
        columns_to_drop_raw=liverpool_columns_to_drop_raw
    else:
        columns_to_drop_raw=championship_columns_to_drop_raw
    columns_to_drop=[normalized_columns[col] for col in columns_to_drop_raw if col in normalized_columns]
    table.drop(columns=columns_to_drop,inplace=True)

    # Remove Summary or duplicate header rows
    table=table[
        ~table.apply(
            lambda row:row.astype(str).str.contains(
            'Squad Total|Opponent Total|Player|Per 90 Minutes|Time|Team Success \\(xG\\)',case=False
            ).any(),axis=1
        )
    ]
    return table

def insert_squad_column(df, squad_name: str = 'Liverpool'):
    """
    Inserts a 'squad' column with a fixed value after 'pos' and before 'age' columns if they exist.
    """
    df = df.copy()
    if 'pos' in df.columns and 'age' in df.columns:
        pos_index = df.columns.get_loc('pos')
        age_index = df.columns.get_loc('age')

        # Insert 'squad' between Pos and Age
        insert_at = min(age_index, pos_index) + 1
        df.insert(loc=insert_at, column='squad', value=squad_name)

    return df
