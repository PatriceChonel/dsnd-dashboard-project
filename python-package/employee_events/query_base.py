# Import any dependencies needed to execute sql queries
import sqlite3
import pandas as pd  # To return data as DataFrame when needed



# Define a class called QueryBase
# Use inheritance to add methods
# for querying the employee_events database.
class QueryBase:


    # Create a class attribute called `name`
    # set the attribute to an empty string
    name = ""#initialize an empty string variable called 'name'

    # Initialize with the database path for connecting
    def __init__(self, db_path="python-package/employee_events/employee_events.db"):#we put in parameter the path
        self.db_path = db_path  # Database file path


    # Define a `names` method that receives
    # no passed arguments
    def names(self):
        # Return an empty list
        return []



    # Define an `event_counts` method
    # that receives an `id` argument
    # This method should return a pandas dataframe
    def event_counts(self, id):

       
        # QUERY 1
        # Write an SQL query that groups by `event_date`
        # and sums the number of positive and negative events
        # Use f-string formatting to set the FROM {table}
        # to the `name` class attribute
        # Use f-string formatting to set the name
        # of id columns used for joining
        # order by the event_date column
        
        query = f"""
            SELECT event_date, 
                   SUM(positive_events) AS positive_events, 
                   SUM(negative_events) AS negative_events
            FROM employee_events
            WHERE {self.name}_id = {id}
            GROUP BY event_date
            ORDER BY event_date
        """
        #Qyery contains the sql query it will return the date of evens, total good events, total of bad events from the table employee_events
        #wewill filter by ID either the team id or employee id
        # we will also group by date of event


        # Execute the query and return as DataFrame
        return pd.DataFrame(self.execute_query(query), columns=["event_date", "positive_events", "negative_events"])


            
    

    # Define a `notes` method that receives an id argument
    # This function should return a pandas dataframe
    def notes(self, id):


        # QUERY 2
        # Write an SQL query that returns `note_date`, and `note`
        # from the `notes` table
        # Set the joined table names and id columns
        # with f-string formatting
        # so the query returns the notes
        # for the table name in the `name` class attribute
        query = f"""
            SELECT note_date, note
            FROM notes
            WHERE {self.name}_id = {id}
        """
        #get the date of when the note was created  and the content of teh note
        # Execute the query and return as DataFrame
        return pd.DataFrame(self.execute_query(query), columns=["Note date", "Note"])

    #utility method to execute an SQL query. I used it in my debugging phase
    #it will be practical this way becase it will centralized the SQL execution and employee that inherit from QueryBase can reuse this method
    def execute_query(self, query):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                return cursor.fetchall()  # Return results as a list of tuples
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []


