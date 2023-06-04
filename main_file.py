''' FUNCTION DEFINITIONS '''


''' CLASS DEFINITIONS'''
# define a bank entry class
class bankEntry:
    __slots__ = {"accountType", "accountNumber", "transactionDate", "amount", "description"}

    # create the class constructor
    def __init__(self, accountType, accountNumber, transactionDate, amount, description) -> None:
        self.accountType = accountType
        self.accountNumber = accountNumber
        self.transactionDate = transactionDate
        self.amount = amount
        self.description = description

    # create the string conversion return type (for printing object data)
    def __str__(self) -> str:
        return f"{self.accountType} | {self.accountNumber} | {self.transactionDate} | {self.amount} | {self.description}"


''' MAIN PROGRAM STARTS HERE '''
test = bankEntry("Chequing", 1, "May 24, 2023", 340, "Initial deposit in bank")

print(test)