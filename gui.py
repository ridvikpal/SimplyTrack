import PySimpleGUI as pg
import mysql_management
import extract_csv
from pathlib import Path
import datetime

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
                pg.Column([[pg.Text("Account Type")], [pg.Input(default_text=y[1], key=(x, 1), pad=(1, 0), size=(30, 1))]], element_justification='center'),
                pg.Column([[pg.Text("Account Number")], [pg.Input(default_text=y[2], key=(x, 2), pad=(1, 0), size=(30, 1))]], element_justification='center'),
                pg.Column([[pg.Text("Transaction Date")], [pg.CalendarButton('Select Date', format='%Y-%m-%d', pad=(1, 0), no_titlebar=False), pg.Input(default_text=y[3], key=(x, 3), pad=(1, 0), size=(15, 1))]], element_justification='center'),
                pg.Column([[pg.Text("Amount")], [pg.Input(default_text=y[4], key=(x, 4), pad=(1, 0), size=(30, 1))]], element_justification='center'),
                pg.Column([[pg.Text("Description")], [pg.Input(default_text=y[5], key=(x, 5), pad=(1, 0), size=(60, 1))]], element_justification='center')
            ])
        else:
            modifyLayout.append([
                pg.Column([[pg.Text(y[0], key=(x, 0))]], element_justification='center'),
                pg.Column([[pg.Input(default_text=y[1], key=(x, 1), pad=(1, 0), size=(30, 1))]], element_justification='center'),
                pg.Column([[pg.Input(default_text=y[2], key=(x, 2), pad=(1, 0), size=(30, 1))]], element_justification='center'),
                pg.Column([[pg.CalendarButton('Select Date', format='%Y-%m-%d', pad=(1, 0), no_titlebar=False), pg.Input(default_text=y[3], key=(x, 3), pad=(1, 0), size=(15, 1))]], element_justification='center'),
                pg.Column([[pg.Input(default_text=y[4], key=(x, 4), pad=(1, 0), size=(30, 1))]], element_justification='center'),
                pg.Column([[pg.Input(default_text=y[5], key=(x, 5), pad=(1, 0), size=(60, 1))]], element_justification='center')
            ])

    # add a horizontal seperator for aesthetics
    modifyLayout.append([pg.HorizontalSeparator()])

    # add the update records button
    modifyLayout.append([
        pg.Column([[pg.Button("Edit All Account Types", key='-ALL_TYPE-')]], element_justification='left'),
        pg.Column([[pg.Button("Edit All Account Numbers", key='-ALL_NUMBER-')]], element_justification='left'),
        pg.Column([[pg.Button("Edit All Transaction Dates", key='-ALL_DATE-')]], element_justification='left'),
        pg.Column([[pg.Button("Edit All Amounts", key='-ALL_AMOUNT-')]], element_justification='left'),
        pg.Column([[pg.Button("Edit All Descriptions", key='-ALL_DESCRIPT-')]], element_justification='left'),
        pg.Column([[pg.Button("Update Records", key='-UPDATE-')]], element_justification='right', expand_x=True)
    ])

    # create the actual window
    modifyWindow = pg.Window("Modify Entries", modifyLayout, resizable=False)

    # main loop for the modify window
    while True:
        event, values = modifyWindow.read()
        # if the window is closed exit without updating
        if event == pg.WIN_CLOSED:
            break
        # if a request is made to update all account types
        if event == '-ALL_TYPE-':
            allDataValue = pg.popup_get_text("Enter the Account Type for all Selected Entries", title="Edit All Account Types")
            for x, y in enumerate(selectData):
                modifyWindow[x, 1].update(allDataValue)
        # if a request is made to update all account numbers
        if event == '-ALL_NUMBER-':
            allDataValue = pg.popup_get_text("Enter the Account Number for all Selected Entries", title="Edit All Account Numbers")
            for x, y in enumerate(selectData):
                modifyWindow[x, 2].update(allDataValue)
        # if a request is made to update all transaction dates
        if event == '-ALL_DATE-':
            allDataValue = pg.popup_get_date(title="Edit All Transaction Dates", no_titlebar=False)
            allDataValue = datetime.date(month=allDataValue[0], day=allDataValue[1], year=allDataValue[2])
            for x, y in enumerate(selectData):
                modifyWindow[x, 3].update(allDataValue)
        # if a request is made to update all amounts
        if event == '-ALL_AMOUNT-':
            allDataValue = pg.popup_get_text("Enter the Amount for all Selected Entries", title="Edit All Amounts")
            for x, y in enumerate(selectData):
                modifyWindow[x, 4].update(allDataValue)
        # if a request is made to update all descriptions
        if event == '-ALL_DESCRIPT-':
            allDataValue = pg.popup_get_text("Enter the Description for all Selected Entries", title="Edit All Descriptions")
            for x, y in enumerate(selectData):
                modifyWindow[x, 5].update(allDataValue)
        # if the update records button is clicked then update them
        if event == '-UPDATE-':
            try:
                for index in range(len(selectData)):
                    newDataToUpdate = [values[index, 1], values[index, 2], values[index, 3], values[index, 4], values[index, 5]]
                    entryID = selectData[index][0]
                    mysql_management.updateDataInSQL(newDataToUpdate, entryID)
                    updateTableGUI(mainWindow)
                break
            except Exception as e:
                pg.popup_error("There was an error updating the values, please ensure the data types are correct:", e, title="An Error Occured")
    modifyWindow.close()

# function to open the custom query GUI
def customQueryGUI() -> None:
    # create the layout for query
    queryLayout = [
        [
            pg.Column([
                [pg.Text("Input")], [pg.Multiline(key='-INPUT-', size=(100, 5))],
                [pg.Text("Output")], [pg.Multiline(key='-OUTPUT-', size=(100, 30))]
            ])
        ],
        [pg.Button("Enter Query", key='-ENTER-')]
    ]

    # create the query Window
    queryWindow = pg.Window("Custom Query", queryLayout, resizable=False)

    # main event loop for query window
    while True:
        event, values = queryWindow.read()
        # if the window is closed exit without updating
        if event == pg.WIN_CLOSED:
            break
        # if the update records button is clicked then update them
        if event == '-ENTER-':
            try:
                result = mysql_management.manualQuery(values['-INPUT-'])
                textOutput = str()
                queryWindow['-OUTPUT-'].update('')
                for x in result:
                    for y in x:
                        textOutput += str(y) + " "
                    textOutput += '\n'
                queryWindow['-OUTPUT-'].update(textOutput)
            except Exception as e:
                pg.popup_error("There was an error executing the query, please ensure the query is correct:", e, title="An Error Occured")
    queryWindow.close()

# function to create the main window (to enable theme switching)
def createMainWindow(colour_theme: pg.theme) -> pg.Window:
    if colour_theme:
        pg.theme(colour_theme)
        if colour_theme == 'DarkGrey13':
            colour_button_text = "Light Mode"
        else:
            colour_button_text = "Dark Mode"

    # setup the layout

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
        pg.Column([[pg.Text("Account Type", auto_size_text=True)], [pg.Input(pad=(1, 0), key='-ACC_TYPE-', size=(30, 1))]], element_justification='center'),
        pg.Column([[pg.Text("Account Number", auto_size_text=True)], [pg.Input(pad=(1, 0), key='-ACC_NUM-', size=(30, 1))]], element_justification='center'),
        pg.Column([[pg.Text("Transaction Date", auto_size_text=True)], [pg.CalendarButton('Select Date', target='-TRANS_DATE-', format='%Y-%m-%d', pad=(1, 0), no_titlebar=False), pg.Input(pad=(1, 0), key='-TRANS_DATE-', size=(15, 1))]], element_justification='center'),
        pg.Column([[pg.Text("Amount", auto_size_text=True)], [pg.Input(pad=(1, 0), key='-AMOUNT-', size=(30, 1))]], element_justification='center'),
        pg.Column([[pg.Text("Description", auto_size_text=True)], [pg.Input(pad=(1, 0), key='-DESCRIPT-', size=(60, 1))]], element_justification='center'),
        pg.Column([[pg.Button("Enter Manual Entry", key='-MAN_ENTRY-', pad=(1, 0))]], vertical_alignment='bottom')
    ]

    # below table layout where controls and info is kept
    belowTable = [
        pg.Column([[pg.Button('Modify Entries', key='-MODIFY-'), pg.Button("Delete Entries", key='-DELETE-'), pg.Button('Import CSV File', key="-CSV-"), pg.Button("Custom Query", key='-QUERY-'), pg.Button(colour_button_text, key="-COLOUR-")]], element_justification='left'),
        pg.Column([[pg.Text("Current Table: main"), pg.Text("Current Database: bank_transactions")]], element_justification='right', expand_x=True),
    ]

    # create the entire gui layout
    layout = [
        [mainTable],
        [belowTable],
        [pg.HorizontalSeparator()],
        [manualEntry]
    ]

    return pg.Window("SimplyTrack", layout, resizable=False)

# this is the data that will be displayed on screen
displayData = list()

# this is the selected data row
selectData = list()

# define the main function
def main() -> None:
    # set the pysimplegui theme
    colour_theme = 'DarkGrey13'

    # update the table data for the first time upon program startup
    updateTableData()

    # create the window
    window = createMainWindow(colour_theme)

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
            except Exception as e:
                pg.popup_error("There was an error importing the csv file, please check the file path and/or csv file:", e, title="An Error Occured")

        # if a deletion was requested, delete the selected rows
        if '-DELETE-' in event:
            try:
                deleteList = list()
                for x in selectData:
                    deleteList.append(x[0])
                mysql_management.deleteDataInSQL(deleteList)
                updateTableGUI(window)
            except Exception as e:
                pg.popup_error("Please make sure you have selected an entry:", e, title="An Error Occured")

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
            except Exception as e:
                pg.popup_error("Please make sure all fields are filled with the correct data type: ", e, title="An Error Occured")

        # if modify data is requested
        if '-MODIFY-' in event:
            modifyGUI(window)

        # if a custom query is requested
        if '-QUERY-' in event:
            customQueryGUI()
        # if a request to toglle between Light/Dark Mode is made
        if '-COLOUR-' in event:
            if colour_theme == 'DarkGrey13':
                colour_theme = 'LightGrey2'
            else:
                colour_theme = 'DarkGrey13'
            window.close()
            window = createMainWindow(colour_theme)
    # At the end of the program, close it
    window.close()

# run the main function
if __name__ == "__main__":
    main()