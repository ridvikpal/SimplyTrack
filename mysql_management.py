''' MODULE IMPORTS '''
import mysql.connector
import mysql_authentication

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

# allows the user to perform a manual query on the database, and returns the result.
def manualQuery(query: str) -> list:
    cursor.execute(query)
    result = list()
    for x in cursor:
        result.append(x)
    return result

''' CONNECT TO SQL DATABASE '''
# credentials for sql server (later ask for from user)

# get the server serverConfiguration
serverConfiguration = mysql_authentication.read_one_block_of_yaml_data('server_configuration')

db = mysql.connector.connect(
    host=serverConfiguration['Host'],
    user=serverConfiguration['Username'],
    passwd=serverConfiguration['Password'],
    database=serverConfiguration['Database']
)

# create our cursor to perform operations
cursor = db.cursor()