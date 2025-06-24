The goal here is to make a dashboard using Streamlit for my Overwatch Data

    
Open `Personal Data Sheets.numbers` into a Pandas Table
    If not possible: exports the `Personal Data Sheets.numbers` into a csv then open in Pandas


Assumptions:

That we can easily placed a sized object anywhere.

We have hovertips like Sigma or Mode for the graphs.

First Edition:

Hard-Coded App w/ pre-set charts and select breakdowns. Mimicing Snowstream.

Overall Long-Term Structure of App: (This code would be easily changeable for other apps)

class DataHouse
    > A figuritive shelf that holds all the different data tables
    Used to be called at the beginning to load the desired csv file

class Container 
    The container we size and fit into a position on the screen
    - Dimensions
    - Border 
    - Background Color (default: none) 
    - Visual 

class Manifest
    A collection of all the different Visuals to choose from
    It is called when a container is created to determine what is being shown

class Visual
    Holds the types of visuals we display in the container (Tabe, Graph, Text, Widget)

class Table
    > A query of a table in DataHouse
    - Dataframe from the query 
    - Table Style
    - Coloring

class Graph
    > A query of a table in DataHouse
    - Dataframe from the query 
    - The Graph of the Data
        Calls a static function on Manifest
    - Graph Style
    - Graph Colors
    - Graph Format

class Text
    Displays a text from a string
    - String
    - Format

class Widget
    Like parameters and filters in Sigma (List, Calemdar, Select)

class List
    Shows a list of options that can be chosen from. Will be multi-select

class Calendar
    Shows a calendar used to pick start_dates and end_dates 

class Switch
    Visual option that allows you to single-select