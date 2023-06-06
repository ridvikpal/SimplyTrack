''' MODULES '''
import csv
import dateutil.parser

''' FUNCTION DEFINITIONS '''
# returns a list of indexes of all matching elements in a list based on partial names string search
def getAllIndexesOfMatchingRow(listToSearch: str, searchKey: str) -> list:
    matchColumns = [x for x in listToSearch if any([searchKey in x, searchKey.lower() in x, searchKey.upper() in x])]
    matchColumnsIndex = list()
    for x in matchColumns:
        matchColumnsIndex.append(listToSearch.index(x))
    return matchColumnsIndex

# returns the first index from left to right of matching elements in a list based on partial names string search
def getSingleIndexOfMatchingRow(listToSearch: str, searchKey: str) -> int:
    matchColumns = [x for x in listToSearch if searchKey in x]
    if len(matchColumns) > 0:
        return listToSearch.index(matchColumns[0])
    return -1

''' CLASS DEFINITIONS'''
# define a bank entry class
class bankEntry:
    __slots__ = ['accountType', 'accountNumber', 'transactionDate', 'amount', 'description']

    # create the class constructor
    def __init__(self, accountType, accountNumber, transactionDate, amount, description) -> None:
        self.accountType = accountType
        self.accountNumber = accountNumber
        self.transactionDate = transactionDate
        self.amount = amount
        self.description = description

    # create the string conversion return type (for printing object data)
    def __str__(self) -> str:
        return f'{self.accountType} | {self.accountNumber} | {self.transactionDate} | {self.amount} | {self.description}'


''' MAIN PROGRAM STARTS HERE '''
# create a list that holds the bank transaction data
allTransactions = list()

# open the bank entries csv file
inputFile = csv.reader(open(r"C:\Users\ridvikpal\Downloads\csv7567.csv", 'r'))

# get the first row which contains the headers of the csv file
firstRow = next(inputFile)

# get the indexes of each type of column to catagorize them
typeIndex = getSingleIndexOfMatchingRow(firstRow, "Account Type")
numberIndex = getSingleIndexOfMatchingRow(firstRow, "Account Number")
dateIndex = getSingleIndexOfMatchingRow(firstRow, "Date")
# get the money based on the type of currency
amountIndex = getSingleIndexOfMatchingRow(firstRow, "$")
if amountIndex < 0:
    amountIndex = getSingleIndexOfMatchingRow(firstRow, "£")
if amountIndex < 0:
    amountIndex = getSingleIndexOfMatchingRow(firstRow, "€")
if amountIndex < 0:
    amountIndex = getSingleIndexOfMatchingRow(firstRow, "₹")
descriptionIndexes = getAllIndexesOfMatchingRow(firstRow, "Description")

# actually process the data in the csv file, and put it into an array of bank entry objects
for row in inputFile:
    descriptionTempList = list()
    accountTypeTemp = row[typeIndex]
    accountNumberTemp = row[numberIndex]
    accountNumberTemp = accountNumberTemp.replace("-", "")
    transactionDateTemp = dateutil.parser.parse(row[dateIndex], ignoretz=True)
    transactionDateTemp = transactionDateTemp.date()
    amountTemp = row[amountIndex]
    for x in descriptionIndexes:
        if len(row[x]) > 0:
            descriptionTempList.append(row[x])
    descriptionTemp = " ".join(descriptionTempList)
    allTransactions.append(bankEntry(accountTypeTemp, accountNumberTemp, transactionDateTemp, amountTemp, descriptionTemp))

# print the bank entry objects for correctness
print("Account Type | Account Number | Transaction Date | Amount | Description")
for x in allTransactions:
    print(x)