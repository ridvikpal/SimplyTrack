import PySimpleGUI as pg
import mysql_management
import datetime

# set the colour theme
# pg.theme('Dark Grey 13')

# everything in our window

data = mysql_management.getDataFromSQL()

displayData = []
for x in data:
    # displayData.append(pg.Text(str(x))
    stringForm = ""
    stringForm += x[0]
    stringForm += " | "
    stringForm += str(x[1])
    stringForm += " | "
    stringForm += x[2].strftime("%Y-%m-%d")
    stringForm += " | "
    stringForm += str(x[3])
    stringForm += " | "
    stringForm += x[4]
    displayData.append(stringForm)

# make the data to display a single string
displayData = '\n'.join([str(i) for i in displayData])

# print(displayData)

layout = [
    [pg.Text(displayData)],
    # [pg.Text("Enter dialog"), pg.InputText()]``
    [pg.Button("Ok"), pg.Button("Cancel")]
]

window = pg.Window("SimplyTrack", layout)

# main event loop to get inputs from input dialogs
while True:
    event, values = window.read()
    if event == pg.WIN_CLOSED or event == "Cancel":
        break
    print("You entered", event[0])

window.close()