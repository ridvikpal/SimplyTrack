import PySimpleGUI as pg
import mysql_management
import extract_csv
from pathlib import Path

# update the table data
def updateTableData() -> None:
    data = mysql_management.getDataFromSQL()
    displayData.clear()
    for x in data:
        y = []
        y.extend([x[0], x[1], x[2], x[3], x[4]])
        displayData.append(y)

# this is the data that will be displayed on screen
displayData = list()

# update the table data for the first time upon program startup
updateTableData()

# headers for table
toprow = [ "Account Type", "Account Number", "Transaction Date", "Amount", "Description" ]

# create the table gui element
mainTable = pg.Table(
                values=displayData, headings=toprow,
                auto_size_columns=True,
                display_row_numbers=True,
                justification='center',
                key='-TABLE-',
                selected_row_colors='blue on black',
                alternating_row_color="grey",
                enable_events=True,
                expand_x=True,
                expand_y=True,
                enable_click_events=True
            )

# create the gui layout
layout = [
   [mainTable],
   [pg.Button('Import CSV File', key="-CSV-")]
]

# create the window
window = pg.Window("SimplyTrack", layout, resizable=True)

# main event loop
while True:
    event, values = window.read() # read both events and values inputted into elements
    # for debugging purposes, print the event and the values
    print("event:", event, "values:", values)
    # if the window is closed, break the main loop
    if event == pg.WIN_CLOSED:
        break
    # if a table element has been clicked do something
    if '+CLICKED+' in event and '-TABLE-' in event:
    #   pg.popup("You clicked row:{} Column: {}".format(event[2][0], event[2][1]))
        pass
    # if csv import button has been clicked do something
    if '-CSV-' in event:
        # try to extract data from the csv file
        try:
            # get the raw csv file path
            raw_path = pg.popup_get_file("Please choose a CSV File", title="Choose CSV File", file_types=(('CSV Files', '*.csv'),))
            # check to make sure there is some raw path
            if raw_path != None:
                # check to make sure the path is not empty
                if len(raw_path) > 0:
                    # get a universal path, irrespective of os platform
                    csv_file_path = Path(raw_path)
                    # extract csv data into bank entry objects
                    transactionsList = extract_csv.extractDataFromCSVFile(csv_file_path)
                    # update those bank entry objects into sql database
                    mysql_management.insertBulkDataIntoSQL(transactionsList)
                    # update the table data
                    updateTableData()
                    # refresh the gui table with new data
                    window["-TABLE-"].update(values=displayData)
        # if there was some error, let the user know
        except:
            pg.popup_error("There was an error importing the csv file, please check the file path and/or csv file", title="An Error Occured")

# At the end of the program, close it
window.close()