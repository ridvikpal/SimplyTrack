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
        y.extend([x[0], x[1], x[2], x[3], x[4], x[5]])
        displayData.append(y)

# update the table data and the actual gui
def updateTableGUI(window: pg.Window) -> None:
    updateTableData()
    window["-TABLE-"].update(values=displayData)

# function to open the modify window
def modifyGUI(mainWindow: pg.Window) -> None:

    # the layout to use for the modify window
    modifyLayout = []

    # add all cells for the window
    for x, y in enumerate(selectData):
        if x == 0:
            modifyLayout.append([
                pg.Column([[pg.Text("ID")], [pg.Text(y[0], key=(x, 0))]], element_justification='center'),
                pg.Column([[pg.Text("Account Type")], [pg.Input(default_text=y[1], key=(x, 1), pad=(1, 0))]], element_justification='center'),
                pg.Column([[pg.Text("Account Number")], [pg.Input(default_text=y[2], key=(x, 2), pad=(1, 0))]], element_justification='center'),
                pg.Column([[pg.Text("Transaction Date")], [pg.CalendarButton('Select Date', format='%Y-%m-%d', pad=(1, 0), no_titlebar=False), pg.Input(default_text=y[3], key=(x, 3), pad=(1, 0))]], element_justification='center'),
                pg.Column([[pg.Text("Amount")], [pg.Input(default_text=y[4], key=(x, 4), pad=(1, 0))]], element_justification='center'),
                pg.Column([[pg.Text("Description")], [pg.Input(default_text=y[5], key=(x, 5), pad=(1, 0))]], element_justification='center')
            ])
        else:
            modifyLayout.append([
                pg.Column([[pg.Text(y[0], key=(x, 0))]], element_justification='center'),
                pg.Column([[pg.Input(default_text=y[1], key=(x, 1), pad=(1, 0))]], element_justification='center'),
                pg.Column([[pg.Input(default_text=y[2], key=(x, 2), pad=(1, 0))]], element_justification='center'),
                pg.Column([[pg.CalendarButton('Select Date', format='%Y-%m-%d', pad=(1, 0), no_titlebar=False), pg.Input(default_text=y[3], key=(x, 3), pad=(1, 0))]], element_justification='center'),
                pg.Column([[pg.Input(default_text=y[4], key=(x, 4), pad=(1, 0))]], element_justification='center'),
                pg.Column([[pg.Input(default_text=y[5], key=(x, 5), pad=(1, 0))]], element_justification='center')
            ])


    # add the update records button
    modifyLayout.append([pg.Button("Update Records", key='-UPDATE-')])

    # create the actual window
    modifyWindow = pg.Window("Test", modifyLayout, resizable=False)

    # main loop for the modify window
    while True:
        event, values = modifyWindow.read()
        # if the window is closed exit without updating
        if event == pg.WIN_CLOSED:
            break
        # if the update records button is clicked then update them
        if event == '-UPDATE-':
            for index in range(len(selectData)):
                newDataToUpdate = [values[index, 1], values[index, 2], values[index, 3], values[index, 4], values[index, 5]]
                # print(newDataToUpdate)
                entryID = selectData[index][0]
                # print(entryID)
                # oldDateToUpdate = [selectData[index][0], selectData[index][1], selectData[index][2], selectData[index][3], selectData[index][4]]
                mysql_management.updateDataInSQL(newDataToUpdate, entryID)
                updateTableGUI(mainWindow)
            break
    modifyWindow.close()

# this is the data that will be displayed on screen
displayData = list()

# this is the selected data row
selectData = list()

# define the main function
def main() -> None:
    # set the pysimplegui theme
    pg.theme('DarkGrey13')

    # update the table data for the first time upon program startup
    updateTableData()

    # headers for table
    tableHeader = [ "ID", "Account Type", "Account Number", "Transaction Date", "Amount", "Description" ]

    # create the table gui element to show the SQL database
    mainTable = pg.Table(
                    values=displayData, headings=tableHeader,
                    auto_size_columns=True,
                    num_rows=30,
                    justification='center',
                    select_mode='extended',
                    key='-TABLE-',
                    selected_row_colors='white on dark blue',
                    # alternating_row_color="dark grey",
                    enable_events=True,
                    expand_x=True,
                    expand_y=True,
                    enable_click_events=True,
                    border_width=4,
                    tooltip="Bank Transactions"
                )

    # create manual entry gui element
    manualEntry = [
        pg.Column([[pg.Text("Account Type", auto_size_text=True)], [pg.Input(pad=(1, 0), key='-ACC_TYPE-', size=(20, 1))]], element_justification='center'),
        pg.Column([[pg.Text("Account Number", auto_size_text=True)], [pg.Input(pad=(1, 0), key='-ACC_NUM-', size=(20, 1))]], element_justification='center'),
        pg.Column([[pg.Text("Transaction Date", auto_size_text=True)], [pg.CalendarButton('Select Date', target='-TRANS_DATE-', format='%Y-%m-%d', pad=(1, 0), no_titlebar=False), pg.Input(pad=(1, 0), key='-TRANS_DATE-', size=(20, 1))]], element_justification='center'),
        pg.Column([[pg.Text("Amount", auto_size_text=True)], [pg.Input(pad=(1, 0), key='-AMOUNT-', size=(20, 1))]], element_justification='center'),
        pg.Column([[pg.Text("Description", auto_size_text=True)], [pg.Input(pad=(1, 0), key='-DESCRIPT-', size=(50, 1))]], element_justification='center'),
        pg.Column([[pg.Button("Enter Manual Entry", key='-MAN_ENTRY-', pad=(1, 0))]], vertical_alignment='bottom')
    ]

    # below table layout where controls and info is kept
    belowTable = [
        pg.Column([[pg.Button('Modify Entries', key='-MODIFY-'), pg.Button("Delete Entries", key='-DELETE-'), pg.Button('Import CSV File', key="-CSV-")]], element_justification='left'),
        pg.Column([[pg.Text("Current Table: main"), pg.Text("Current Database: bank_transactions")]], element_justification='right', expand_x=True),
    ]

    # create the entire gui layout
    layout = [
        [mainTable],
        [belowTable],
        [pg.HorizontalSeparator()],
        [manualEntry]
    ]

    # create the window
    window = pg.Window("SimplyTrack", layout, resizable=False)

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
            # print(selectData)

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
                        updateTableGUI(window)
            # if there was some error, let the user know
            except:
                pg.popup_error("There was an error importing the csv file, please check the file path and/or csv file", title="An Error Occured")

        # if a deletion was requested, delete the selected rows
        if '-DELETE-' in event:
            try:
                deleteList = list()
                for x in selectData:
                    deleteList.append(x[0])
                mysql_management.deleteDataInSQL(deleteList)
                updateTableGUI(window)
            except:
                pg.popup_error("Please make sure you have selected an entry", title="An Error Occured")

        # if a manual entry is entered into the system
        if '-MAN_ENTRY-' in event:
            try:
                # first make sure all entries are filled
                transaction = [values['-ACC_TYPE-'], values['-ACC_NUM-'], values['-TRANS_DATE-'], values['-AMOUNT-'], values['-DESCRIPT-']]
                if values['-ACC_TYPE-'] and values['-ACC_NUM-'] and values['-TRANS_DATE-'] and values['-AMOUNT-'] and values['-DESCRIPT-']:
                    mysql_management.insertDataIntoSQL(transaction)
                    updateTableGUI(window)
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
            modifyGUI(window)
    # At the end of the program, close it
    window.close()

# run the main function
if __name__ == "__main__":
    main()