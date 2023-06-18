import matplotlib.pyplot as plt
import itertools

def showGraph(data: list, theme: str):
    with plt.style.context(theme):
        # setup the account data dictionary
        accountData = dict()
        for x in data:
            if x[2] not in accountData.keys():
                accountData.update({x[2]: None})

        # create a matplotlib figure to house the plot in
        graphFigure = plt.figure("Graph of Account Balance")
        graphFigure.set_figheight(8)
        graphFigure.set_figwidth(14)

        # add data to the account data dictionary
        for x in accountData:
            yData = list()
            xData = list()
            for y in data:
                if y[2] == x:
                    xData.append(y[3])
                    yData.append(y[4])
            xData.sort()
            yData = list(itertools.accumulate(yData)) # add up all the transactions
            accountData[x] = [xData, yData]
            plt.plot(xData, yData, label=x)

        # actually show the graph
        plt.legend(title="Account Number", fancybox=True)
        plt.xlabel("Date")
        plt.ylabel("Amount ($)")
        plt.title("Account Balance", loc='center')
        plt.tight_layout()

        plt.show()