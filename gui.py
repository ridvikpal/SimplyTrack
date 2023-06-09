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

# update the table data and the actual gui
def updateTableGUI() -> None:
    updateTableData()
    window["-TABLE-"].update(values=displayData)

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

manualEntry = [
    [pg.Text("Account Type: "), pg.Input(key='-ACC_TYPE-', justification='left')],
    [pg.Text("Account Number: "), pg.Input(key='-ACC_NUM-', justification='left')],
    [pg.Text("Transaction Date: "), pg.CalendarButton('Select', target='-TRANS_DATE-', format='%Y-%m-%d'), pg.Input(key='-TRANS_DATE-', justification='left')],
    [pg.Text("Amount: "), pg.Input(key='-AMOUNT-', justification='left')],
    [pg.Text("Description: "), pg.Input(key='-DESCRIPT-', justification='left')],
    [pg.Button('Add Manual Entry', key='-MAN_ENTRY-')]
]

csvImport = [pg.Button('Import CSV File', key="-CSV-")]

# create the gui layout
layout = [
   [mainTable],
   [manualEntry, csvImport]
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
                    updateTableGUI()
        # if there was some error, let the user know
        except:
            pg.popup_error("There was an error importing the csv file, please check the file path and/or csv file", title="An Error Occured")

    # if the calendar button is pressed
    # if '-TRANS_DATE_SELECT-' in event:
    #     values['-TRANS_DATE-'] = values['-TRANS_DATE_SELECT']
    #     window["-TABLE-"].update()

    # if a manual entry is entered
    if 'MAN_ENTRY' in event:
        try:
            # first make sure all entries are filled
            accType, accNum, transDate, amount, description = values['-ACC_TYPE-'], values['-ACC_NUM-'], values['-TRANS_DATE-'], values['-AMOUNT-'], values['-DESCRIPT-']
            if values['-ACC_TYPE-'] and values['-ACC_NUM-'] and values['-TRANS_DATE-'] and values['-AMOUNT-'] and values['-DESCRIPT-']:
                mysql_management.insertDataIntoSQL(accType,accNum, transDate, amount, description)
                updateTableGUI()
                window['-ACC_TYPE-']('')
                window['-ACC_NUM-']('')
                window['-TRANS_DATE-']('')
                window['-AMOUNT-']('')
                window['-DESCRIPT-']('')
            else:
                pg.popup_error("Please make sure all fields are filled", title="An Error Occured")
        except:
            pg.popup_error("Please make sure all fields are filled with the correct data type", title="An Error Occured")
# At the end of the program, close it
window.close()