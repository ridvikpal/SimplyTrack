''' MODULES '''
import csv

''' FUNCTION DEFINITIONS '''
# returns a list of indexes of all matching elements in a list based on partial names string search
def getIndexOfMatchingRow(listToSearch: str, searchKey: str) -> list:
    matchColumns = [x for x in listToSearch if any([searchKey in x, searchKey.lower() in x, searchKey.upper() in x])]
    matchColumnsIndex = []
    for x in matchColumns:
        matchColumnsIndex.append(listToSearch.index(x))
    return matchColumnsIndex

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
allTransactions = []

# test = bankEntry('Chequing', 1, 'May 24, 2023', 340, 'Initial deposit in bank')

# get the bank entries from the csv file
# first open the csv file
inputFile = csv.reader(open(r'C:\Users\ridvikpal\Downloads\csv94961.csv', 'r'))

# get the first row which contains the headers of the csv file
firstRow = next(inputFile)

# get the indexes of each type of column to catagorize them
typeIndex = []
numberIndex = []
dateIndex = []
amountIndex = []
descriptionIndex = []
typeIndex.extend(getIndexOfMatchingRow(firstRow, "Account Type"))
numberIndex.extend(getIndexOfMatchingRow(firstRow, "Account Number"))
dateIndex.extend(getIndexOfMatchingRow(firstRow, "Date"))
amountIndex.extend(getIndexOfMatchingRow(firstRow, "$"))
amountIndex.extend(getIndexOfMatchingRow(firstRow, "£"))
amountIndex.extend(getIndexOfMatchingRow(firstRow, "€"))
amountIndex.extend(getIndexOfMatchingRow(firstRow, "₹"))
descriptionIndex.extend(getIndexOfMatchingRow(firstRow, "Description"))

# get the account number row
print('Account Type: ', typeIndex)
print('Account Number: ', numberIndex)
print('Transaction Date: ', dateIndex)
print('Amount: ', amountIndex)
print('Description: ', descriptionIndex)