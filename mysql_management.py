''' MODULE IMPORTS '''
import extract_csv
import mysql.connector

''' FUNCTION DEFINITIONS '''
# inserts given bank entries into the SQL database
def insertDataIntoSQL(transactionList: list) -> None:
    for x in transactionList:
        cursor.execute(f"insert into main values(\"{x[0]}\", {x[1]}, \"{x[2]}\", {x[3]}, \"{x[4]}\")")
    db.commit()

# retrieves data from sql database
def getDataFromSQL(lastYear: bool = True) -> list():
    if lastYear == False:
        cursor.execute("select * from main")
    else:
        cursor.execute("select * from main where transaction_date between date_sub(now(), interval 1 year) and now();")

    sqlData = list()
    for x in cursor:
        sqlData.append(x)
    return sqlData

''' CONNECT TO SQL DATABASE '''
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="MclarenP1",
    database="bank_transactions"
)

# create our cursor to perform operations
cursor = db.cursor()