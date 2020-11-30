import pandas as pd
from sqlalchemy import create_engine
# make sure to pip install python packages: lxml, sqlalchemy, pymysql


# function to create a database connection
def connect_to_sql():
    sql_engine = create_engine('mysql+pymysql://root:root@localhost:8889/CNA330')
    db_connection = sql_engine.connect()
    return db_connection


# Read the data from web
jobs = pd.read_html("https://www.bls.gov/oes/2019/may/oes_nat.htm")[1]

# Remove empty rows
jobs = jobs.dropna()
jobs = jobs.where(pd.notnull(jobs), None)

# Remove duplicate rows
jobs = jobs.drop_duplicates()

# Convert 'dollar' columns from '$2000,000.00' to float 2000000
jobs['Median hourly wage'] = jobs['Median hourly wage'].replace('[$,()]', '', regex=True)
jobs['Median hourly wage'] = jobs['Median hourly wage'].astype(float)
jobs['Annual mean wage'] = jobs['Annual mean wage'].replace('[$,()]', '', regex=True)
jobs['Annual mean wage'] = jobs['Annual mean wage'].astype(float)
jobs['Mean hourly wage'] = jobs['Mean hourly wage'].replace('[$,()]', '', regex=True)
jobs['Mean hourly wage'] = jobs['Mean hourly wage'].astype(float)
jobs['Employment per 1,000 jobs'] = jobs['Employment per 1,000 jobs'].round(decimals=3)

# Remove boring columns
jobs = jobs.drop(axis='columns', labels='Occupation code')

# Rename columns: shorten if too long, remove '(' and ')' characters, replace ' ' spaces with '_'
jobs.rename(columns=lambda x: x[:25].strip(), inplace=True)
jobs.rename(columns=lambda x: x.replace(' ', '_').replace('(', '').replace(')', ''), inplace=True)

# Insert the data into mysql table, replace if already exists
jobs.to_sql('job_salaries', con=connect_to_sql(), if_exists='replace', index=False)
