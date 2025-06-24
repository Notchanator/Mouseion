import pandas as pd

class Groomer:
    # Takes care of all the opening and formatting of the data table.

    table: pd.DataFrame

    def __init__(self, file):
        file_name = self.covert_to_CSV(file)
        self.table = pd.read_csv(file_name)
        

    def convertToCSV(self, file):
        # TO DO
        return "Personal_Data_Sheets.csv"
        
    
class Tree:
    # Holds all the different queries.

    original_table: pd.DataFrame

    def __init__(self, )
     