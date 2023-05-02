import sqlite3
import pandas as pd
import psycopg2
import os

# directories:
imports_path = "/sqlite_imports/"
exports_path = "/flat_census_exports/"

# Join tables are simply id:name with a non-capitalized, pluralized naming convention for table name
# dict to match relational_column_id:related_table
tables_to_join = {
    'sex_id':             "sexes",
    'race_id':            "races",
    'country_id':         "countries",
    'workclass_id':       "workclasses",
    'occupation_id':      "occupations",
    'marital_status_id':  "marital_statuses",
    'education_level_id': "education_levels"
}

# base select statement, all local fields to records table, could easily have another mapping dict or simple list for this
select_clause = "SELECT records.id, records.age, records.education_num, records.capital_gain, records.capital_loss, records.hours_week, records.over_50k"

# base join statement
join_clause = ""

for t in tables_to_join.items():

    # build out the select statement. Append an aliased name field for each pertinent join table to select statement
    # created aliases for columns will be same as original field heads, but _id replaced with _name
    select_clause += ", " + t[1] + ".name AS " + t[0][:-3] + "_name"

    # build out the join statement. 
    join_clause += " LEFT JOIN " + t[1] + " ON records." + t[0] + " = " + t[1] + ".id"

# syntax together our select and join clauses to get our full query
flat_pull_sql = select_clause + " FROM records " + join_clause

# Iterate through all of the .sqlite files found in /sqlite_imports
# for each one, export its flat representation as a csv into /flat_census_exports
i = 0
for sqlite in os.scandir(imports_path):
    if sqlite.path[-7:] == ".sqlite":
        conn = sqlite3.connect(sqlite.path)
        flat_dataframe = pd.read_sql_query(
            flat_pull_sql,
            conn
        )
        conn.close()
        csv = flat_dataframe.to_csv(exports_path + str(i) + '.csv', index=False)
        i += 1

print("Flattened " + str(i) + " sqlite databases")

# postgres connection details
pg_host     = os.environ["POSTGRES_HOST"] or "localhost"
pg_dbname   = "postgres"
pg_user     = "postgres"
pg_password = os.environ["POSTGRES_PASSWORD"] or "postgres"

pg_conn = psycopg2.connect(host=pg_host, dbname=pg_dbname, user=pg_user, password=pg_password)

pg_cur = pg_conn.cursor()
# first drop table to normalize initial conditions
pg_cur.execute("DROP TABLE IF EXISTS records")
pg_cur.execute(""" 
    CREATE TABLE records(
        id integer PRIMARY KEY,
        age integer,
        education_num integer,
        capital_gain integer,
        capital_loss integer,
        hours_week integer,
        over_50k boolean,
        sex text,
        race text,
        country text,
        workclass text,
        occupation text,
        marital_status text,
        education_level text
    )
""")

# Iterate through all of the .csv files found in /flat_census_exports, and import them into postgres
i = 0
for flat_census in os.scandir(exports_path):
    with open(flat_census.path, 'r') as f:
        # skip header row, columns are ordered
        next(f)
        pg_cur.copy_from(f, 'records', sep=",")
        i += 1

pg_conn.commit()

print("Imported " + str(i) + " census docs into postgres.")

