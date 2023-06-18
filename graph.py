import matplotlib.pyplot as plt
import itertools
import numpy as np

def on_pick(event):
    annotation_visibility = dataPointAnnotation.get_visible()
    if annotation_visibility:
        dataPointAnnotation.set_visible(False)
    line = event.artist
    xdata, ydata = line.get_data()
    ind = event.ind
    xPoint = xdata[ind][0]
    yPoint = ydata[ind][0]

    dataPointAnnotation.xy = (xPoint, yPoint)
    text_label = "(" + xPoint.strftime("%Y-%m-%d") + ", " + "{:.2f}".format(yPoint) + ")"
    dataPointAnnotation.set_text(text_label)
    if graphTheme == 'classic':
        dataPointAnnotation.get_bbox_patch().set_facecolor('white')
    else:
        dataPointAnnotation.get_bbox_patch().set_facecolor('black')
    dataPointAnnotation.set_visible(True)
    graphFigure.canvas.draw_idle()


def showGraph(data: list, theme: str):
    global graphFigure
    global ax
    global dataPointAnnotation
    global graphTheme
    graphTheme = theme
    with plt.style.context(theme):
        # setup the account data dictionary
        accountData = dict()
        for x in data:
            if x[2] not in accountData.keys():
                accountData.update({x[2]: None})

        # create a matplotlib figure to house the plot in
        graphFigure = plt.figure("Graph of Account Balance")
        ax = graphFigure.add_subplot(111)
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
            plt.plot(xData, yData, label=x, marker='o', picker=5)

        dataPointAnnotation = ax.annotate(
            text='',
            xy=(0, 0),
            xytext=(-20, 20), # distance from x, y
            textcoords='offset points',
            ha='center',
            bbox={'boxstyle': 'round', 'fc': 'w'},
            arrowprops={'arrowstyle': '->'}
        )
        dataPointAnnotation.set_visible(False)

        cid = graphFigure.canvas.mpl_connect('pick_event', on_pick)

        # actually show the graph
        plt.legend(title="Account Number", fancybox=True)
        plt.xlabel("Date")
        plt.ylabel("Amount ($)")
        plt.title("Account Balance", loc='center')
        plt.tight_layout()

        plt.show()