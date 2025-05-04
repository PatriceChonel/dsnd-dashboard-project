# Create a subclass of base_components/MatplotlibViz
# called `LineChart`
class LineChart(MatplotlibViz):

    
    # Overwrite the parent class's `visualization`
    # method. Use the same parameters as the parent
    def visualization(self, model, asset_id):
        




        # Pass the `asset_id` argument to
        # the model's `event_counts` method to
        # receive the x (Day) and y (event count)
        data = model.event_counts(asset_id)

        
        # Use the pandas .fillna method to fill nulls with 0
        data = data.fillna(0)

        
        # User the pandas .set_index method to set
        # the date column as the index
        data = data.set_index("event_date")

        
        # Sort the index
        data = data.sort_index()
        
        # Use the .cumsum method to change the data
        # in the dataframe to cumulative counts
        data = data.cumsum()

        
        
        # Set the dataframe columns to the list
        # ['Positive', 'Negative']
        data.columns = ["Positive", "Negative"]

        
        # Initialize a pandas subplot
        # and assign the figure and axis
        # to variables
        fig, ax = plt.subplots()

        
        # call the .plot method for the
        # cumulative counts dataframe
        data.plot(ax=ax)

        
        # pass the axis variable
        # to the `.set_axis_styling`
        # method
        # Use keyword arguments to set 
        # the border color and font color to black. 
        # Reference the base_components/matplotlib_viz file 
        # to inspect the supported keyword arguments
        self.set_axis_styling(ax, border_color="black", font_color="black")

        
        # Set title and labels for x and y axis
        ax.set_title("Event Counts Over Time")
        ax.set_xlabel("Day")
        ax.set_ylabel("Event Count")
        return fig



# Create a subclass of base_components/MatplotlibViz
# called `BarChart`
class BarChart(MatplotlibViz):


    # Create a `predictor` class attribute
    # assign the attribute to the output
    # of the `load_model` utils function
    predictor = load_model()

    # Overwrite the parent class `visualization` method
    # Use the same parameters as the parent
    def visualization(self, model, asset_id):
        



        # Using the model and asset_id arguments
        # pass the `asset_id` to the `.model_data` method
        # to receive the data that can be passed to the machine
        # learning model
        data = model.model_data(asset_id)

       
        
        # Using the predictor class attribute
        # pass the data to the `predict_proba` method
        proba = self.predictor.predict_proba(data)

        
        # Index the second column of predict_proba output
        # The shape should be (<number of records>, 1)
        proba = proba[:, 1]

        
        
        # Below, create a `pred` variable set to
        # the number we want to visualize
        #
        # If the model's name attribute is "team"
        # We want to visualize the mean of the predict_proba output
        pred = proba.mean() if model.name == "team" else proba[0]

            
        # Otherwise set `pred` to the first value
        # of the predict_proba output


        
        # Initialize a matplotlib subplot
        fig, ax = plt.subplots()
        
        # Run the following code unchanged
        ax.barh([''], [pred])
        ax.set_xlim(0, 1)
        ax.set_title('Predicted Recruitment Risk', fontsize=20)
        
        # pass the axis variable
        # to the `.set_axis_styling`
        # method
        self.set_axis_styling(ax, border_color="black", font_color="black")

        return fig
