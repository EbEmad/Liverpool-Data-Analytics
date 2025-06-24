from scraping.scrap_data import scrape_tables
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import sys
from pathlib import Path
import pandas as pd
from scraping.clean_data import flatten_columns, clean_table, insert_squad_column

# Create database engine
engine = create_engine(f"postgresql://user:root@postgres:5432/test_db")


# Define the XPATH for the Championship table
championship_xpath = '/html/body/div[4]/div[6]/div[3]/div[4]/table'

# URLs to scrape
urls = {
    "Standard_Stats": "https://fbref.com/en/comps/10/stats/Championship-Stats",
    "Goalkeeping": "https://fbref.com/en/comps/10/keepers/Championship-Stats",
    "Advanced_Goalkeeping": "https://fbref.com/en/comps/10/keepersadv/Championship-Stats",
    "Shooting": "https://fbref.com/en/comps/10/shooting/Championship-Stats",
    "Passing": "https://fbref.com/en/comps/10/passing/Championship-Stats",
    "Pass_Types": "https://fbref.com/en/comps/10/passing_types/Championship-Stats",
    "Goal_Shot_Creation": "https://fbref.com/en/comps/10/gca/Championship-Stats",
    "Defensive_Actions": "https://fbref.com/en/comps/10/defense/Championship-Stats",
    "Possession": "https://fbref.com/en/comps/10/possession/Championship-Stats",
    "Playing_Time": "https://fbref.com/en/comps/10/playingtime/Championship-Stats",
    "Miscellaneous_Stats": "https://fbref.com/en/comps/10/misc/Championship-Stats",
    "Liverpool": "https://fbref.com/en/squads/822bd0ba/Liverpool-Stats"
}

tables_names = [
    'Standard_Stats',
    'Scores_Fixtures',
    'Goalkeeping',
    'Advanced_Goalkeeping',
    'Shooting',
    'Passing',
    'Pass_Types',
    'Goal_Shot_Creation',
    'Defensive_Actions',
    'Possession',
    'Playing_Time',
    'Miscellaneous_Stats'
]

with engine.begin() as conn:
    for tbl in tables_names:
        table_name=f"stg_{tbl}"
        conn.execute(text(f'DROP TABLE IF EXISTS "public"."{table_name}";'))
    print("Dropped all staging tables.")

# scrap and explore data

for name,url in urls.items():
    if name=='Liverpool':
        tables=scrape_tables(url,club=name,sleep_time=10)
    
        if tables:
            print('-'*20)
            print(len(tables),end=' ')
            print('tables_found')
            for i,table in enumerate(tables[0:12]):
                # flatten the table if it is a DataFrame
                table=flatten_columns(table)
                table=clean_table(club=name,table=table)
                # Insert the squad column for
                table = insert_squad_column(table, squad_name="Liverpool")
                # get the table name
                table_name = f"stg_{tables_names[i]}"
                # Store the table in the database
                table.to_sql(table_name, engine, schema="public", if_exists='append', index=False)
                print("-"*20)
                print(f"Table {i+1} ({table_name}) inserted successfully.")

    else:
      
        table = scrape_tables(url=url, club=name, xpath=championship_xpath)
        # Check if the table is empty
        if  table is None or not hasattr(table, "empty") or table.empty:
            print("-" * 20)
            print(f"❌ No tables found for {name}")
            continue

        print("-" * 20)
        print(f"Found the table for the Championship's players \"{name}\" data")
        # flatten the table if it is a DataFrame
        table=flatten_columns(table)
        table=clean_table(club=name,table=table)
        # Get the table name
        table_name = f"stg_{name}"
        # Store the table in the database
        table.to_sql(table_name, engine, schema="public", if_exists='replace', index=False)

        print(f"✅ Loaded Championship's players \"{name}\" data into \"{table_name}\"")


# Finish the scraping process
print("-" * 20)
print("🏁 Data exploration and loading completed.")