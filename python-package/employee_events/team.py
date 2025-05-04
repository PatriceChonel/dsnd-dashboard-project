# Import the QueryBase class
from .query_base import QueryBase  # As specified in the assignment

# Import dependencies for SQL execution
from .sql_execution import QueryMixin  # Assumes QueryMixin is used for query-related methods
import pandas as pd  #  import pandas since it’s used below


# Create a subclass of QueryBase
# called  `Team`
class Team(QueryBase, QueryMixin):  # Uses inheritance to add query-related methods

    # Set the class attribute `name`
    # to the string "team"
    name = "Team"


    #I added an __init__method to set the databasepath
    def __init__(self, db_path=None):
        if db_path:
            self.db_path = db_path
        else:
            # path of the Database
            self.db_path = "C:/Users/chone/anaconda3/project/Advanced/dsnd-dashboard-project/python-package/employee_events/employee_events.db"


    # Define a `names` method
    # that receives no arguments
    # This method should return
    # a list of tuples from an SQL execution
    def names(self):
        query = """
            SELECT team_name, team_id
            FROM team
        """
        return self.query(query)

    # Define a `username` method
    # that receives an ID argument
    # This method should return
    # a list of tuples from an SQL execution
    def username(self, id):
        query = """
            SELECT team_name
            FROM team
            WHERE team_id = ?
        """
        return self.query(query, (id,))


    # Below is a method with an SQL query
    # This SQL query generates the data needed for
    # the machine learning model.
    # Without editing the query, alter this method
    # so when it is called, a Pandas DataFrame
    # is returned containing the execution of
    # the SQL query
    def model_data(self, id):
        # SQL query string that will:
        # Join the 'team' and 'employee_events' tables on 'team_id'
        # Filter for a specific team_id (provided as parameter '?')
        # Group results by employee_id to aggregate event counts
        # Calculate SUM of positive_events and negative_events per employee
        #SQL query to aggregate positive/negative events per employee in a specific team
        query = """
            SELECT positive_events, negative_events FROM (
                SELECT employee_id,
                    SUM(positive_events) AS positive_events,
                    SUM(negative_events) AS negative_events
                FROM team
                JOIN employee_events
                    USING(team_id)
                WHERE team.team_id = ?
                GROUP BY employee_id
            )
        """
        return pd.DataFrame(self.pandas_query(query, (id,)), columns=["positive_events", "negative_events"])
        # Return the query results as a cleaned pandas DataFrame