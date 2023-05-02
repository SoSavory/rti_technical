# rti_technical

Overview:

1. A bash script polls the "sqlite_imports" dir for changes. If there are no changes, proceed to (5), else, proceed to (2).
2. A python script constructs a query which is applied to each sqlite db found in the "sqlite_imports" dir. 
   This query joins all tables associated to the "records" table.
3. The python script then creates a csv from query results from (2) and saves them to "flat_census_exports".
4. The python script imports these generated csv files into a running postgres db.
5. A simple rails application spins up (at localhost:3000), providing an arbitrarily chosen summary of the data, as well as a paginated view of records.
