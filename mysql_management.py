''' MODULE IMPORTS '''
import main_file
import mysql.connector

''' FUNCTION DEFINITIONS '''
# inserts given bank entries into the SQL database
def insertDataIntoSQL(transactionList: list) -> None:
    for x in transactionList:
        a = x.accountType
        b = x.accountNumber
        c = x.transactionDate
        d = x.amount
        e = x.description
        # print(f"insert into main values("{x.accountType}", {x.transactionDate})")
        cursor.execute(f"insert into main values(\"{a}\", {b}, \"{c}\", {d}, \"{e}\")")
           # print(f"insert into main values(\"{a}\", {b}, {c}, {d}, \"{e}\")")
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

''' MAIN PROGRAM STARTS HERE '''
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="MclarenP1",
    database="bank_transactions"
)

cursor = db.cursor()

# insertDataIntoSQL(main_file.allTransactions)

test = getDataFromSQL()

# cursor.execute("select * from main")

# for x in cursor:
#     print(x)

print(test[2])