''' MODULE IMPORTS'''
import PySimpleGUI as pg
import mysql_management
import extract_csv
from pathlib import Path
import datetime
import graph

''' FUNCTION DEFINITIONS '''
# update the table data
def updateTableData() -> None:
    data = mysql_management.getDataFromSQL()
    displayData.clear()
    for x in data:
        y = []
        y.extend([x[0], x[1], x[2], x[3], x[4], x[5]])
        displayData.append(y)

# update the table data and the actual table gui
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
                pg.popup_ok("Please ensure the data types are correct for each field:", e, title="An Error Occured")
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
                pg.popup_ok("Please ensure the query is correct:", e, title="An Error Occured")
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

    # below table layout where controls and info is kept
    belowTable = [
        pg.Column([[pg.Button('Modify Entries', key='-MODIFY-'), pg.Button("Delete Entries", key='-DELETE-'), pg.Button('Import CSV File', key="-CSV-"), pg.Button("Graph Data", key='-GRAPH-'), pg.Button("Custom Query", key='-QUERY-'), pg.Button(colour_button_text, key="-COLOUR-")]], element_justification='left'),
        pg.Column([[pg.Text("Current Table: " + mysql_management.table), pg.Text("Current Database: " + mysql_management.db.database)]], element_justification='right', expand_x=True),
    ]

    # create manual entry gui element
    manualEntry = [
        pg.Column([[pg.Button("Autofill Data", key='-AUTOFILL-', pad=(1, 0))]], vertical_alignment='bottom'),
        pg.Column([[pg.Text("Account Type", auto_size_text=True)], [pg.Input(pad=(1, 0), key='-ACC_TYPE-', size=(30, 1))]], element_justification='center'),
        pg.Column([[pg.Text("Account Number", auto_size_text=True)], [pg.Input(pad=(1, 0), key='-ACC_NUM-', size=(30, 1))]], element_justification='center'),
        pg.Column([[pg.Text("Transaction Date", auto_size_text=True)], [pg.CalendarButton('Select Date', target='-TRANS_DATE-', format='%Y-%m-%d', pad=(1, 0), no_titlebar=False), pg.Input(pad=(1, 0), key='-TRANS_DATE-', size=(15, 1))]], element_justification='center'),
        pg.Column([[pg.Text("Amount", auto_size_text=True)], [pg.Input(pad=(1, 0), key='-AMOUNT-', size=(30, 1))]], element_justification='center'),
        pg.Column([[pg.Text("Description", auto_size_text=True)], [pg.Input(pad=(1, 0), key='-DESCRIPT-', size=(60, 1))]], element_justification='center'),
        pg.Column([[pg.Button("Enter Manual Entry", key='-MAN_ENTRY-', pad=(1, 0))]], vertical_alignment='bottom')
    ]

    # create the entire gui layout
    layout = [
        [mainTable],
        [belowTable],
        [pg.HorizontalSeparator()],
        [manualEntry]
    ]

    return pg.Window("SimplyTrack", layout, resizable=False)

# function to create the startup dialog box gui that allows the user to create a yaml SQL configuration file
def databaseInfoGUI() -> dict:
    # set the theme
    pg.theme('DarkGrey13')

    # data to return
    data = dict()

    # create the layout
    dbLayout = []

    dbLayout.append([pg.Column([
        [pg.Column([[pg.Text("Please enter the database configuration information. "
                 "This will be stored in a server_configuration.yaml file to store this for later", size=(45,3))]])],
        [pg.Column([[pg.Text("Username")], [pg.Text("Password")], [pg.Text("Hostname")], [pg.Text("Database")], [pg.Text("Table")]]),
        pg.Column([[pg.Input(key="-USER-")], [pg.Input(key="-PASSWD-", password_char='*')], [pg.Input(key="-HOST-")], [pg.Input(key="-DB-")], [pg.Input(key="-TB-")]])]
    ])])

    dbLayout.append([
        pg.Column([[pg.Radio("Use Existing Database and Table", "database", default=True)], [pg.Radio("Create Database and Table", "database", key='-NEW_DB-')], [pg.Radio("Create Table", "database", key='-NEW_TB-')]], expand_x=True, expand_y=True, element_justification='left'),
        pg.Column([[pg.Button("Create YAML File", key="-CREATE-")]], element_justification='right')
    ])

    dbWindow = pg.Window("Enter Database Information", dbLayout, resizable=False)

    # main event loop for query window
    while True:
        event, values = dbWindow.read()
        # if the window is closed exit without updating
        if event == pg.WIN_CLOSED:
            exit()
        # if the update records button is clicked then update them
        if event == '-CREATE-':
            username = values['-USER-']
            password = values['-PASSWD-']
            host = values['-HOST-']
            database = values['-DB-']
            table = values['-TB-']
            # get the values of whether or not we are creating a database/table
            newDB = values['-NEW_DB-']
            newTB = values['-NEW_TB-']
            # make sure all fields are full
            if username and password and host and database and table:
                data = {
                    'Username' : username,
                    'Host' : host,
                    'Database' : database,
                    'Table' : table
                }
                break
            else:
                pg.popup_ok("Please ensure all fields are filled:", title="An Error Occured")
    dbWindow.close()
    return data, newDB, newTB, password # return the data

# new yaml file setup and start the program
def newDatabaseConnection() -> None:
    while True:
        # create the config file
        information = databaseInfoGUI()
        serverConfiguration = information[0]
        newDB = information[1]
        newTB = information[2]
        password = information[3]
        mysql_management.write_yaml_to_file(serverConfiguration, 'server_configuration')

        # create the new encrypted password
        mysql_management.encrypt.generateKey()
        mysql_management.encrypt.generateEncryptedPassword(password)

        # attempt to connect to the database
        try:
            mysql_management.setupSQL(serverConfiguration)

            # connect to the right database
            if newDB == True: # if a new database should be created
                mysql_management.setupDatabase(serverConfiguration['Database'], new=True)
                mysql_management.setupTable(serverConfiguration['Table'], new=True)
            elif newTB == True:
                mysql_management.setupDatabase(serverConfiguration['Database'])
                mysql_management.setupTable(serverConfiguration['Table'], new=True)
            else:
                mysql_management.setupDatabase(serverConfiguration['Database'])
                mysql_management.setupTable(serverConfiguration['Table'])

            return # after succesful connection, exit function
        except Exception as e:
            pg.popup_ok("The data entered was incorrect, please provide the correct data", e, title="Incorrect Data")

            # remove the incorrect server configuration file and then restart the loop
            serverConfigurationPath = Path("server_configuration.yaml")
            serverConfigurationPath.unlink()

# this is the data that will be displayed on screen
displayData = list()

# this is the selected data row
selectData = list()

# define the main function
def main() -> None:
    # set the pysimplegui initial theme
    colour_theme = 'DarkGrey13'

    # set the initial font size
    pg.set_options(font=("Arial", 11))

    # setup the server with the config file
    configFile = Path("server_configuration.yaml")
    serverConfiguration = dict()

    # if the config file exists
    if configFile.is_file():
        # attempt to read the server configuration file and load the database
        try:
            serverConfiguration = mysql_management.read_one_block_of_yaml_data(configFile)
            mysql_management.setupSQL(serverConfiguration)
            mysql_management.setupDatabase(serverConfiguration['Database'])
            mysql_management.setupTable(serverConfiguration['Table'])
        except Exception as e:
            # inform user the server configuration file is corrupt
            pg.popup_ok("There is an error in the data in the server_configuration.yaml file:", e,
                        "You will be prompted to enter the correct database information to recreate the file", title="Incorrect YAML File")
            # setup a new, correct server configuration file
            configFile.unlink() # remove the existing server_configuration file
            newDatabaseConnection()
    # else the config file does not exist
    else:
        newDatabaseConnection()

    # once a connection has been established, now start and use the program

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
                pg.popup_ok("Please check the file path and/or csv file:", e, title="An Error Occured")

        # if a deletion was requested, delete the selected rows
        if '-DELETE-' in event:
            try:
                deleteList = list()
                for x in selectData:
                    deleteList.append(x[0])
                mysql_management.deleteDataInSQL(deleteList)
                updateTableGUI(window)
            except Exception as e:
                pg.popup_ok("Please make sure you have selected an entry:", e, title="An Error Occured")

        # if manual entry autofill was requested
        if '-AUTOFILL-' in event:
            try:
                window['-ACC_TYPE-'](selectData[0][1])
                window['-ACC_NUM-'](selectData[0][2])
                window['-TRANS_DATE-'](selectData[0][3])
                window['-AMOUNT-'](selectData[0][4])
                window['-DESCRIPT-'](selectData[0][5])
            except Exception as e:
                pg.popup_ok("Please make sure you have selected a data reference from the table to autofill from", e, title="An Error Occured")
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
                    pg.popup_ok("Please make sure all fields are filled", title="An Error Occured")
            except Exception as e:
                pg.popup_ok("Please make sure all fields are filled with the correct data type: ", e, title="An Error Occured")

        # if modify data is requested
        if '-MODIFY-' in event:
            if selectData:
                modifyGUI(window)
            else:
                pg.popup_ok("Please make sure you have selected entries", title="An Error Occured")

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

        # if a graph was requested
        if '-GRAPH-' in event:
            if colour_theme == 'DarkGrey13':
                graph.showGraph(displayData, 'dark_background')
            else:
                graph.showGraph(displayData, 'classic')


    # At the end of the program, close it
    window.close()

# run the main function
if __name__ == "__main__":
    main()