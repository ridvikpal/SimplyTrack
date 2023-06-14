''' MODULE IMPORTS '''
import extract_csv
import mysql.connector
from decimal import Decimal
import datetime

''' FUNCTION DEFINITIONS '''
# inserts multiple bank entries (transactions) into the SQL database
def insertBulkDataIntoSQL(transactionList: list) -> None:
    for x in transactionList:
        add_entry = ("insert into main(account_type, account_number, transaction_date, amount, description) values(%s, %s, %s, %s, %s)")
        # cursor.execute(f"insert into main values(\"{x[0]}\", {x[1]}, \"{x[2]}\", {x[3]}, \"{x[4]}\")")
        cursor.execute(add_entry, x)
    db.commit()

# inserts one single bank entry (transaction) into the SQL database
def insertDataIntoSQL(transaction: list) -> None:
    add_entry = ("insert into main(account_type, account_number, transaction_date, amount, description) values(%s, %s, %s, %s, %s)")
    cursor.execute(add_entry, transaction)
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

# deletes an entry from the sql database
def deleteDataInSQL(transactionIDList: list) -> None:
    # transactionIDList.sort(reverse=True)
    delete_entry = ("delete from main where id = %s")
    for x in transactionIDList:
        cursor.execute(delete_entry, (x,))
    db.commit()

# update existing records in a table
def updateDataInSQL(newData: list, entryID: int) -> None:
    update_entry = ("update main set "
                    "account_type = %s, account_number = %s, "
                    "transaction_date = %s, amount = %s, "
                    "description = %s where "
                    "id = %s")
    combinedList = newData
    combinedList.append(entryID)
    cursor.execute(update_entry, combinedList)
    db.commit()

def manualQuery(query: str) -> str:
    cursor.execute(query)

    pass

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