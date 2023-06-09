''' MODULE IMPORTS '''
import extract_csv
import mysql.connector
from decimal import Decimal
import datetime

''' FUNCTION DEFINITIONS '''
# inserts multiple bank entries (transactions) into the SQL database
def insertBulkDataIntoSQL(transactionList: list) -> None:
    for x in transactionList:
        cursor.execute(f"insert into main values(\"{x[0]}\", {x[1]}, \"{x[2]}\", {x[3]}, \"{x[4]}\")")
    db.commit()

# inserts one single bank entry (transaction) into the SQL database
def insertDataIntoSQL(acc_type: str, acc_number: int, trans_date: datetime.date, amount: Decimal, description: str) -> None:
    cursor.execute(f"insert into main values(\"{acc_type}\", {acc_number}, \"{trans_date}\", {amount}, \"{description}\")")
    db.commit()

# retrieves data from sql database
def getDataFromSQL(lastYear: bool = False) -> list():
    if lastYear == False:
        cursor.execute("select * from main")
    else:
        cursor.execute("select * from main where transaction_date between date_sub(now(), interval 1 year) and now();")

    sqlData = list()
    for x in cursor:
        sqlData.append(x)
    return sqlData

''' CONNECT TO SQL DATABASE '''
# credentials for sql server (later ask for from user)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="MclarenP1",
    database="bank_transactions"
)

# create our cursor to perform operations
cursor = db.cursor()