import PySimpleGUI as pg
import mysql_management
import extract_csv
from pathlib import Path

# set the colour theme
# pg.theme('Dark Grey 13')

# everything in our window

def updateTable():
    data = mysql_management.getDataFromSQL()
    listData = []
    for x in data:
        y = []
        y.extend([x[0], x[1], x[2], x[3], x[4]])
        listData.append(y)
    return listData

# make the data to display a single string
# displayData = '\n'.join([str(i) for i in displayData])

# update the table for the first time upon program startup
displayData = updateTable()

toprow = [ "Account Type", "Account Number", "Transaction Date", "Amount", "Description" ]
# print(toprow)
# print(data)

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

layout = [
   [mainTable],
   [pg.Button('Import CSV File', key="-CSV-")]
]

window = pg.Window("SimplyTrack", layout, resizable=True)
csv_file_path = ""

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
        try:
            # get the csv file path
            raw_path = pg.popup_get_file("Please choose a CSV File", title="Choose CSV File", file_types=(('CSV Files', '*.csv'),))
            if raw_path != None:
                if len(raw_path) > 0:
                    csv_file_path = Path(raw_path)
                    # upload the csv file to the SQL database
                    transactions = extract_csv.extractDataFromCSVFile(csv_file_path)
                    mysql_management.insertDataIntoSQL(transactions)
                    displayData = updateTable()
                    window["-TABLE-"].update(values=displayData)
        except:
            pg.popup_error("There was an error importing the csv file, please check the file path and/or csv file", title="An Error Occured")

# At the end of the program, close it
window.close()