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

def modifyGUI() -> None:

    modifyHeader = [
        pg.Text("Account Type"),
        pg.Text("Account Number"),
        pg.Text("Transaction Date"),
        pg.Text("Amount"),
        pg.Text("Description")
    ]

    modifyLayout = [modifyHeader]

    for x in selectData:
        modifyLayout.append([
            pg.Input(),
            pg.Input(),
            pg.Input(),
            pg.Input(),
            pg.Input(),
        ])

    modifyWindow = pg.Window("Test", modifyLayout, resizable=True)

    while True:
        event, values = modifyWindow.read()
        if event == pg.WIN_CLOSED:
            break

    modifyWindow.close()

# this is the data that will be displayed on screen
displayData = list()

# update the table data for the first time upon program startup
updateTableData()

# this is the selected data row
selectData = list()

# headers for table
header = [ "Account Type", "Account Number", "Transaction Date", "Amount", "Description" ]

# create the table gui element
mainTable = pg.Table(
                values=displayData, headings=header,
                auto_size_columns=True,
                display_row_numbers=True,
                justification='center',
                select_mode='extended',
                key='-TABLE-',
                selected_row_colors='white on dark blue',
                alternating_row_color="grey",
                enable_events=True,
                expand_x=True,
                expand_y=True,
                enable_click_events=True,
                tooltip="Bank Transactions"
            )

# create manual entry gui element
manualEntry = [
    [pg.Text("Account Type: "), pg.Input(key='-ACC_TYPE-', justification='left')],
    [pg.Text("Account Number: "), pg.Input(key='-ACC_NUM-', justification='left')],
    [pg.Text("Transaction Date: "), pg.CalendarButton('Select', target='-TRANS_DATE-', format='%Y-%m-%d'), pg.Input(key='-TRANS_DATE-', justification='left')],
    [pg.Text("Amount: "), pg.Input(key='-AMOUNT-', justification='left')],
    [pg.Text("Description: "), pg.Input(key='-DESCRIPT-', justification='left')],
    [pg.Button('Add Manual Entry', key='-MAN_ENTRY-')]
]

# create delete entries button
deleteEntries = [pg.Button("Delete Entries", key='-DELETE-')]

# create csv import button
csvImport = [pg.Button('Import CSV File', key="-CSV-")]

# create the modify button
modifyEntriesButton = [pg.Button('Modify Entries', key='-MODIFY-')]

# create the entire gui layout
layout = [
   [mainTable],
   [manualEntry, csvImport],
   [deleteEntries],
   [modifyEntriesButton]
]

# create the window
window = pg.Window("SimplyTrack", layout, resizable=True)

# main event loop
while True:
    event, values = window.read() # read both events and values inputted into elements
    # for debugging purposes, print the event and the values
    # print("event:", event, "values:", values)

    # if the window is closed, break the main loop
    if event == pg.WIN_CLOSED:
        break

    # if a table event has been clicked, store the clicked rows in selectData
    if event == '-TABLE-':
        selectData.clear()
        for x in values['-TABLE-']:
            selectData.append(displayData[x])

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

    # if a deletion was requested, delete the selected rows
    if '-DELETE-' in event:
        try:
            for x in selectData:
                accType, accNum, transDate, amount, description = x
                mysql_management.deleteDataInSQL(accType, accNum, transDate, amount, description)
            updateTableGUI()
        except:
            pg.popup_error("Please make sure you have selected an entry", title="An Error Occured")

    # if a manual entry is entered into the system
    if '-MAN_ENTRY-' in event:
        try:
            # first make sure all entries are filled
            accType, accNum, transDate, amount, description = values['-ACC_TYPE-'], values['-ACC_NUM-'], values['-TRANS_DATE-'], values['-AMOUNT-'], values['-DESCRIPT-']
            if values['-ACC_TYPE-'] and values['-ACC_NUM-'] and values['-TRANS_DATE-'] and values['-AMOUNT-'] and values['-DESCRIPT-']:
                mysql_management.insertDataIntoSQL(accType,accNum, transDate, amount, description)
                updateTableGUI()
                # clear input fields
                window['-ACC_TYPE-']('')
                window['-ACC_NUM-']('')
                window['-TRANS_DATE-']('')
                window['-AMOUNT-']('')
                window['-DESCRIPT-']('')
            else:
                pg.popup_error("Please make sure all fields are filled", title="An Error Occured")
        except:
            pg.popup_error("Please make sure all fields are filled with the correct data type", title="An Error Occured")

    if '-MODIFY-' in event:
        modifyGUI()
# At the end of the program, close it
window.close()