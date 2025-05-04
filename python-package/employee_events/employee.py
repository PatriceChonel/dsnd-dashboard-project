# Modifications performed in this employee.py file  
# - Imports the necessary modules (QueryBase and execute_query)  
# - Defines the Employee class, inheriting from QueryBase  
# - Implements username(id) to return an employee's full name using an ID  
# - Converts RAW SQL results into a Pandas DataFrame  
import sqlite3
import pandas as pd

# Import the QueryBase class  
from .query_base import QueryBase  # As requested in the assignment  

# Import dependencies needed for SQL execution  
from .sql_execution import QueryMixin  # As requested in the assignment  


# Define a subclass of QueryBase called Employee  
class Employee(QueryBase, QueryMixin):  
    # Set the class attribute `name` to "employee"  
    name = "Employee"  

    #debugging
    def __init__(self, db_path=None):
        # Initialize the database path and allow an override from the argument
        if db_path:
            self.db_path = db_path
        else:
            self.db_path = "C:/Users/chone/anaconda3/project/Advanced/dsnd-dashboard-project/python-package/employee_events/employee_events.db"


    # Define a method called `names`  
    # This method returns a list of tuples from an SQL execution  
    def names(self):  
        query = """  
            SELECT first_name || ' ' || last_name AS full_name, employee_id  
            FROM employee  
        """  
        return self.query(query)  

    # Define a method called `username`  
    # Retrieves an employee's full name using an ID  
    def username(self, id):  
        query = f"""  
            SELECT first_name || ' ' || last_name AS full_name  
            FROM employee  
            WHERE employee_id = {id}  
        """  
        return self.query(query)  

    # This method retrieves SQL data for the machine learning model  
    # Converts the result into a Pandas DataFrame  
    #import pandas as pd  # As requested in the assignment  

    def model_data(self, id):  
        query = f"""  
            SELECT SUM(positive_events) AS positive_events,  
                   SUM(negative_events) AS negative_events  
            FROM {self.name}  
            JOIN employee_events  
                USING({self.name}_id)  
            WHERE {self.name}.{self.name}_id = {id}  
        """  
        return self.pandas_query(query)  # Use `pandas_query` from QueryMixin



employee = Employee()  
print(employee.names()) 
