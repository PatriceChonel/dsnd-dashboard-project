from fasthtml.common import *#this will import all functions methods, classes from the basic module fasthtml.common
import matplotlib.pyplot as plt#import pyply of matplotlib for the visuals
import pandas as pd  # Import pandas for DataFrame manipulationexit()
import sqlite3#import sqlite3 for the database connection
import sys#import the sys modul to access the system functionnality
import os#import OS modul for OS interaction

# Ensure I set the correct absolute path for the database employee_evends.db
db_path = "C:/Users/chone/anaconda3/project/Advanced/dsnd-dashboard-project/python-package/employee_events/employee_events.db"
sys.path.append(os.path.abspath("C:/Users/chone/anaconda3/project/Advanced/dsnd-dashboard-project/python-package"))


# Use this path whenever connecting to sqlite in  script
def get_connection():
    """Returns a database connection."""
    conn = sqlite3.connect(db_path)
    return None


# Import QueryBase, Employee, Team from employee_events
from employee_events import QueryBase, Employee, Team


# import the load_model function from the utils.py file
from utils import load_model


"""
Below, we import the parent classes
you will use for subclassing
"""
from base_components import (# Importing various UI components from the base_components module
    Dropdown,# A dropdown/select menu component for user selection
    BaseComponent,# A foundational class that other components inherit from
    Radio,# Radio button component for single-option selection
    MatplotlibViz,# Component for embedding Matplotlib visualizations
    DataTable# Component for displaying tabular data in a table format
    )

from combined_components import FormGroup, CombinedComponent


# Create a subclass of base_components/dropdown
# called `ReportDropdown`
class ReportDropdown(Dropdown):

    
    # Overwrite the build_component method
    # ensuring it has the same parameters
    # as the Report parent class's method
    def build_component(self,*args):
       

        #  Set the `label` attribute so it is set
        #  to the `name` attribute for the model
        if len(args) == 2:  
            entity_id, model = args
        else:
            model = args[0]  # If extra argument is passed, ignore it
            entity_id = None 
        
        self.label = model.name  

        
        # Return the output from the
        # parent class's build_component method
        return super().build_component(entity_id, model)


    
    # Overwrite the `component_data` method
    # Ensure the method uses the same parameters
    # as the parent class method
    def component_data(self,entity_id, model):
        
        # Using the model argument
        # call the employee_events method
        # that returns the user-type's
        # names and ids
        return model.names()


# Create a subclass of base_components/BaseComponent
# called `Header`
class Header(BaseComponent):

    # Overwrite the `build_component` method
    # Ensure the method has the same parameters
    # as the parent class
    def build_component(self,entity_id, model):

 
        # Using the model argument for this method
        # return a fasthtml H1 objects
        # containing the model's name attribute
        return H1(f"{model.name} performance")  # Combine model.name + "performance" as requested in the assessment. the title will change accordingly of the choice of the user between team and employe



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
        #data = data.set_index("event_date")
        data["event_date"] = pd.to_datetime(data["event_date"])
        data.set_index("event_date", inplace=True)

                
        # Sort the index
        data = data.sort_index()
       
       
        # Set the dataframe columns to the list
        # ['Positive', 'Negative']
 
        data.rename(columns={"positive_events": "Positive", "negative_events": "Negative"}, inplace=True)

        # Validate that required columns exist
        if not set(["Positive", "Negative"]).issubset(data.columns):
            raise KeyError("ERROR: Missing required columns in DataFrame before cumulative sum.")


        # Ensure numeric values before cumulative sum
        data[["Positive", "Negative"]] = data[["Positive", "Negative"]].apply(pd.to_numeric, errors="coerce")

        # Use the .cumsum method to change the data
        # in the dataframe to cumulative counts
        data[['Positive', 'Negative']] = data[['Positive', 'Negative']].cumsum()
        
        
        # Initialize a pandas subplot
        # and assign the figure and axis
        # to variables
        fig, ax = plt.subplots()


        # Ensure there is numeric data to plot
        if data.empty:
            raise ValueError("ERROR: No numeric data available to plot.")

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
        self.set_axis_styling(ax, bordercolor="black", fontcolor="black")

        
        # Set title and labels for x and y axis
        ax.set_title("Event Counts Over Time", fontsize=15)#set_title will display the title we also set the fontsize to 15
        ax.set_xlabel(" ")#setting the label for the x axis to none because it is obvious it is the months
        ax.set_ylabel("Event Count")#setting the label for the y axis
        return fig #display the plot



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
        ax.set_xlim(0, 1)#we set the limits of the x axis from 0 to 1. 0 is a low risk and 1 is high risk
        ax.set_title('Risk of an employee being recruited by another company', fontsize=15)# we set the title of the plot and the size of the font
        ax.set_xlabel('Probability of losing the employee')#seting the x label. we do not need the y label as there is only one bar for this chart
        # pass the axis variable
        # to the `.set_axis_styling`
        # method
        self.set_axis_styling(ax, bordercolor="black", fontcolor="black")#we set the border and the font color to black

        return fig

 
# Create a subclass of combined_components/CombinedComponent
# called Visualizations       
class Visualizations(CombinedComponent):


    # Set the `children`
    # class attribute to a list
    # containing an initialized
    # instance of `LineChart` and `BarChart`
    children = [LineChart(), BarChart()]


    # Leave this line unchanged
    outer_div_type = Div(cls='grid')
            
# Create a subclass of base_components/DataTable
# called `NotesTable`
class NotesTable(DataTable):


    # Overwrite the `component_data` method
    # using the same parameters as the parent class
    def component_data(self, model, entity_id):

        
        # Using the model and entity_id arguments
        # pass the entity_id to the model's .notes 
        # method. Return the output
         # If 'model' does not have a 'notes' attribute but 'entity_id' does,
        # then the parameters are swapped. So swap them.
        if not hasattr(model, "notes") and hasattr(entity_id, "notes"):
            model, entity_id = entity_id, model

        note_content = model.notes(entity_id)
        # Wrap the note content in a Div with a top margin
        wrapped_note = Div(note_content, style="margin-top:20px;")

        return model.notes(entity_id)


    

class DashboardFilters(FormGroup):

    id = "top-filters"
    action = "/update_data"
    method="POST"

    children = [
        Radio(
            values=["Employee", "Team"],
            name='profile_type',
            hx_get='/update_dropdown',
            hx_target='#selector'
            ),
        ReportDropdown(
            id="selector",
            name="user-selection")
        ]
    
# Create a subclass of CombinedComponents
# called `Report`
class Report(CombinedComponent):

    # Set the `children`
    # class attribute to a list
    # containing initialized instances 
    # of the header, dashboard filters,
    # data visualizations, and notes table
    children = [Header(), DashboardFilters(), Visualizations(), NotesTable()]


# Initialize a fasthtml app 
app = FastHTML()


# Initialize the `Report` class
report = Report()



# Create a route for a get request
# Set the route's path to the root
@app.get("/")
def homepage():
    entity_id = "1"  # debug nsure it's a string if needed
    model = Employee()  # debug explicitly create an instance


    # Call the initialized report
    # pass the integer 1 and an instance
    # of the Employee class as arguments
    # Return the result
 
    return report(1, Employee())



# Create a route for a get request
# Set the route's path to receive a request
# for an employee ID so `/employee/2`
# will return the page for the employee with
# an ID of `2`. 
# parameterize the employee ID 
# to a string datatype
@app.get("/employee/{id}")
def employee_page(id: str):


    # Call the initialized report
    # pass the ID and an instance
    # of the Employee SQL class as arguments
    # Return the result
    return report(id, Employee())


# Create a route for a get request
# Set the route's path to receive a request
# for a team ID so `/team/2`
# will return the page for the team with
# an ID of `2`. 
# parameterize the team ID 
# to a string datatype
@app.get("/team/{id}")
def team_page(id: str):


    # Call the initialized report
    # pass the id and an instance
    # of the Team SQL class as arguments
    # Return the result
    return report(id, Team())



# Keep the below code unchanged!
@app.get('/update_dropdown{r}')
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    print('PARAM', r.query_params['profile_type'])
    if r.query_params['profile_type'] == 'Team':
        return dropdown(None, Team())
    elif r.query_params['profile_type'] == 'Employee':
        return dropdown(None, Employee())


@app.post('/update_data')
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data._dict['profile_type']
    id = data._dict['user-selection']
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == 'Team':
        return RedirectResponse(f"/team/{id}", status_code=303)
    



serve()