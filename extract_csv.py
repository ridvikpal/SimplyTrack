''' MODULE IMPORTS '''
import csv
from pathlib import Path
import dateutil.parser
from decimal import Decimal

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

def extractDataFromCSVFile(filePath: Path) -> list():
    inputFile = csv.reader(open(filePath, 'r'))
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

    # description may have multiple indexes, so get all of them
    descriptionIndexes = getAllIndexesOfMatchingRow(firstRow, "Description")

    # create a list that holds the bank transaction data
    allTransactionsList = list()

    # actually process the data in the csv file, and put it into an 2d array
    for row in inputFile:
        # transaction = [ "Account Type", "Account Number", "Transaction Date", "Amount", "Description" ]
        transaction = list()
        transaction.append(row[typeIndex])
        transaction.append(row[numberIndex])
        transaction[-1] = transaction[-1].replace("-", "")
        transaction.append((dateutil.parser.parse(row[dateIndex], ignoretz=True)).date())
        transaction.append(Decimal(row[amountIndex]))

        # combine all description strings into one sigle string
        transaction.append("")
        for x in descriptionIndexes:
            if len(row[x]) > 0:
                transaction[-1] += row[x]
                transaction[-1] += " "
        transaction[-1] = transaction[-1].strip()
        allTransactionsList.append(transaction)
    return allTransactionsList