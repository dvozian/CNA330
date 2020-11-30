# CNA330
# Group7 Project Pandas Salaries
# Participants: Dorin Vozian, Vlado Situm, Abdirizak Kulmie
# Tutoring Liviu Patrasco liviu_patrasco@hotmail.com


import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as pp
import sys


# function to create a database connection
def connect_to_sql():
    sql_engine = create_engine('mysql+pymysql://root:root@localhost:8889/CNA330')
    db_connection = sql_engine.connect()
    return db_connection


def get_jobs_from_database(search_keyword):
    search_sql = "select * from job_salaries " \
                 "where lower(Occupation_title_click_o) like '%" + search_keyword + \
                 "%' limit 30"
    print(search_sql)
    jobs = pd.read_sql(
        search_sql,
        connect_to_sql())
    return jobs


def plot_jobs(jobs):
    jobs.plot(x="Occupation_title_click_o", y='Annual_mean_wage', kind='barh')
    jobs.plot(x="Employment_per_1,000_jobs", y='Occupation_title_click_o', kind='scatter')
    pp.show()


def main():
    if len(sys.argv) > 1:
        search_keyword = sys.argv[1]
    else:
        search_keyword = 'computer'

    jobs = get_jobs_from_database(search_keyword)

    plot_jobs(jobs)


if __name__ == '__main__':
    main()
