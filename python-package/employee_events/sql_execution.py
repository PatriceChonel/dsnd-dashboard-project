#The code is like a set of tools for working with the employee_events.db database
#we will be to get results in two formats Dataframe and list of tuples for raw sql results

from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd

# Using pathlib, create a `db_path` variable
# that points to the absolute path for the `employee_events.db` file
db_path = "C:/Users/chone/anaconda3/project/Advanced/dsnd-dashboard-project/python-package/employee_events/employee_events.db"





# OPTION 1: MIXIN
# Define a class called `QueryMixin`
class QueryMixin:
    
    # Define a method named `pandas_query`
    # that receives an sql query as a string
    # and returns the query's result
    # as a pandas dataframe
    def pandas_query(self, sql_query, params=()):
        try:# try to run the database query and return results
            with connect(db_path) as connection:
                return pd.read_sql_query(sql_query, connection, params=params)# run the sql query with parameters convert results to pandas dataframe
        except Exception as e:# if there's any error print the error message return empty dataframe if query fails
            print(f"Error executing query: {e}")
            return pd.DataFrame()

    # Define a method named `query`
    # that receives an sql_query as a string
    # and returns the query's result as
    # a list of tuples. (You will need
    # to use an sqlite3 cursor)
    def query(self, sql_query, params=()):
        with connect(db_path) as connection:# open connection to database file
            cursor = connection.cursor()# create cursor to interact with database
            cursor.execute(sql_query, params)  #in my studies in Cybersecurity we learn to improve the safety by preventing any SQL injection from hackers
            return cursor.fetchall() # get all results from query


    

 
 # Leave this code unchanged
def query(func):
    """
    Decorator that runs a standard sql execution
    and returns a list of tuples
    """

    @wraps(func)
    def run_query(*args, **kwargs):
        query_string = func(*args, **kwargs)
        connection = connect(db_path)
        cursor = connection.cursor()
        result = cursor.execute(query_string).fetchall()
        connection.close()
        return result
    
    return run_query
