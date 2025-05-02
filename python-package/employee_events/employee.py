# Modifications performed in this employee.py file  
# - Imports the necessary modules (QueryBase and execute_query)  
# - Defines the Employee class, inheriting from QueryBase  
# - Implements username(id) to return an employee's full name using an ID  
# - Converts RAW SQL results into a Pandas DataFrame  

# Import the QueryBase class  
from .query_base import QueryBase  # As requested in the assignment  

# Import dependencies needed for SQL execution  
from .sql_execution import QueryMixin  # As requested in the assignment  

# Define a subclass of QueryBase called Employee  
class Employee(QueryBase, QueryMixin):  
    # Set the class attribute `name` to "employee"  
    name = "employee"  

    # Define a method called `names`  
    # This method returns a list of tuples from an SQL execution  
    def names(self):  
        query = """  
            SELECT first_name || ' ' || last_name AS full_name, employee_id  
            FROM employee  
        """  
        return query(query)  

    # Define a method called `username`  
    # Retrieves an employee's full name using an ID  
    def username(self, id):  
        query = f"""  
            SELECT first_name || ' ' || last_name AS full_name  
            FROM employee  
            WHERE employee_id = {id}  
        """  
        return query(query)  

    # This method retrieves SQL data for the machine learning model  
    # Converts the result into a Pandas DataFrame  
    import pandas as pd  # As requested in the assignment  

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
