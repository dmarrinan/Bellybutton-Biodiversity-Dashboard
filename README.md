# Belly Button Dashboard

## Purpose
This dashboard shows plots for various subjects in an experiment looking at what organisms live in their belly buttons.

app.py is a flask app that returns jsonified queries from the sqlite database. The sqlite database contains information on samples found in the bellybuttons of all the subjects of the experiment. It also contains information on all the organisms found throughout the experiment. It is used to return all the data needed for the dashboard. Finally it contains metadata about the subjects of the experiment.

## Requirements
This notebook requires python to be installed. Python 3.6.2 was used during development. SQLAlchemy was used to query the databases in python. Flask was used to host the app to return the data for the plots in json format. All required libraries can be found in requirements.txt and installed with the following command: <br/>
<br/>
`pip install requirements.txt -r` <br/>
<br/>

## Running the Code
To run the flask app type the following into the command line: <br/>
<br/>
`python app.py` <br/>
<br/>
Copy the local address listed into your browser and it will render the html page. Use the dropdown menu to switch between different subjects from the study.

## Link to App
https://morning-sands-91050.herokuapp.com/
