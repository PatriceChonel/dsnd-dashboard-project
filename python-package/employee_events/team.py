# Import the QueryBase class
from .query_base import QueryBase  # As specified in the assignment

# Import dependencies for SQL execution
from .sql_execution import QueryMixin  # Assumes QueryMixin is used for query-related methods

# Create a subclass of QueryBase
# called  `Team`
class Team(QueryBase, QueryMixin):  # Uses inheritance to add query-related methods

    # Set the class attribute `name`
    # to the string "team"
    name = "team"

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
        query = f"""
            SELECT team_name
            FROM team
            WHERE team_id = {id}
        """
        return self.query(query)

    # Below is a method with an SQL query
    # This SQL query generates the data needed for
    # the machine learning model.
    # Without editing the query, alter this method
    # so when it is called, a Pandas DataFrame
    # is returned containing the execution of
    # the SQL query
    def model_data(self, id):
        query = f"""
            SELECT positive_events, negative_events FROM (
                SELECT employee_id,
                       SUM(positive_events) AS positive_events,
                       SUM(negative_events) AS negative_events
                FROM {self.name}
                JOIN employee_events
                    USING({self.name}_id)
                WHERE {self.name}.{self.name}_id = {id}
                GROUP BY employee_id
            )
        """
        return self.pandas_query(query)  # Returns the result as a Pandas DataFrame