''' MODULE IMPORTS '''
import mysql.connector
import yaml
import encrypt

''' FUNCTION DEFINITIONS '''
# inserts multiple bank entries (transactions) into the SQL database
def insertBulkDataIntoSQL(transactionList: list) -> None:
    for x in transactionList:
        add_entry = "insert into " + table + ("(account_type, account_number, transaction_date, amount, description) values(%s, %s, %s, %s, %s)")
        # cursor.execute(f"insert into table values(\"{x[0]}\", {x[1]}, \"{x[2]}\", {x[3]}, \"{x[4]}\")")
        cursor.execute(add_entry, x)
    db.commit()

# inserts one single bank entry (transaction) into the SQL database
def insertDataIntoSQL(transaction: list) -> None:
    add_entry = "insert into " + table + ("(account_type, account_number, transaction_date, amount, description) values(%s, %s, %s, %s, %s)")
    cursor.execute(add_entry, transaction)
    db.commit()

# retrieves data from sql database
def getDataFromSQL(lastYear: bool = False) -> list():
    if lastYear == False:
        cursor.execute("select * from " + table)
    else:
        # this query only retrieves the last year's entries, but is not really used, for a future feature
        cursor.execute("select * from " + table + " where transaction_date between date_sub(now(), interval 1 year) and now();")

    return cursor.fetchall()

# deletes an entry from the sql database
def deleteDataInSQL(transactionIDList: list) -> None:
    # transactionIDList.sort(reverse=True)
    delete_entry = ("delete from " + table + " where id = %s")
    for x in transactionIDList:
        cursor.execute(delete_entry, (x,))
    db.commit()

# update existing records in a table
def updateDataInSQL(newData: list, entryID: int) -> None:
    update_entry = "update " + table + (" set "
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

# function to write yaml file
def write_yaml_to_file(data,filename) -> None:
    with open(f'{filename}.yaml', 'w',) as f :
        yaml.dump(data,f,sort_keys=False)
    # print('Written to file successfully')

# function to read one block of a yaml file and returns it as a dictionary
def read_one_block_of_yaml_data(file) -> dict:
    with open(file,'r') as f:
        output = yaml.safe_load(f)
    return output

# function to setup the database and connect to mySQL
def setupSQL(data: dict) -> None:
    # first get the encrypted password from the binary file and decrypt it
    password = encrypt.decryptEncryptedPassword()

    # create a global database object
    global db
    db = mysql.connector.connect(
        host=data['Host'],
        user=data['Username'],
        passwd=password
        # database=data['Database']
    )

    # create a global cursor object
    global cursor
    cursor = db.cursor()

# setup the database we will use
def setupDatabase(name: str, new:bool = False) -> None:
    if new == True:
        # statement = ("create database %s") # for some reason this doesn't work???
        cursor.execute("create database " + name)
        db.commit()
    db.database = name

# set up the table we will use
def setupTable(name: str, new: bool = False) -> None:
    global table
    if new == True:
        statement = "create table " + name + ("(id mediumint not null auto_increment, "
                       "account_type mediumtext, account_number bigint, "
                       "transaction_date date, amount double precision, "
                       "description longtext, primary key(id))")
        # statement = ("create table %s(id mediumint not null auto_increment, " # doesn't work for some reason
        #                "account_type mediumtext, account_number bigint, "
        #                "transaction_date date, amount double precision, "
        #                "description longtext, primary key(id))")
        cursor.execute(statement)
        db.commit()
    table = name