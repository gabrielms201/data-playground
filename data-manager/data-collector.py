import datetime as dt
import matplotlib as mpl
import matplotlib.dates as md
import matplotlib.pyplot as plt
import numpy as np

# Metric Class
class Metric():
    def __init__(self, name, type, column):
        self.type = type.upper()
        self.column = column
        self.__name = name
        self.__content = []
    
    # Content getter && setter
    def setContent(self, data, line):
        if self.type == "NUMERIC":
            data = data[line][self.column].replace(",", ".").replace(" ", "0").replace('"', "")
            return self.__content.append(float(data))
        elif self.type == "DATE":
            time = data[line][self.column].replace('"', "")
            dateFormat = "%m/%d/%Y %H:%M"
            if len(time) <= 16:
                return self.__content.append(dt.datetime.strptime(time, dateFormat))
            else:
                return self.__content.append(dt.datetime.strptime(time, dateFormat + ":%S.%f"))
    def getContent(self):
        return self.__content
    # Name getter
    def getName(self):
        return self.__name

class DataBase():
    def __init__(self, metrics):
        self.__metrics = metrics

    # Data getter && setter
    def setData(self, filename):
        file = open(filename, "r", encoding="UTF-8")
        data = [line.rstrip("\n") for line in file]
        data = [words.split("\t") for words in data]
        file.close()
        self.__data = data
        self.fileName = filename
    def getData(self):
        return self.__data
    # Metrics getter
    def getMetrics(self):
        return self.__metrics
    # Custom methods
    def fillMetrics(self): # Idea: Try to reduce the complexity of this algorithm
        for metric in self.__metrics:
            for line in range(1, len(self.__data)):
                metric.setContent(self.__data, line)

class Graphic:
    def __init__(self, data):
        self.__data = data
    
    def viewGraphicData(self, x, y, shoudPlot = False, scatterColor = "blue", scatterSize = 5, linewidth = 1, plotColor = "red"):
        xContent = x.getContent()
        yContent = y.getContent()

        ax=plt.gca()
        ax.set_xticks(xContent)
        mpl.rcParams["figure.dpi"] = 150
        ax.xaxis.set_major_formatter(md.DateFormatter("%H:%M"))
        plt.xticks(rotation = 90, size = 8)
        plt.locator_params(axis="x", nbins=(len(xContent)/3))
        plt.locator_params(axis="y", nbins=(len(yContent)/10))

        plt.scatter(xContent, yContent, color = scatterColor, s = scatterSize)
        if shoudPlot: 
            plt.plot(xContent, yContent, color = plotColor, linewidth = linewidth)
        
        # Labels && Legends
        plt.title(self.__data.fileName)
        plt.ylabel(y.getName())
        plt.xlabel(x.getName())
        plt.grid(alpha = 0.5)
        plt.show()

def main():
    # Metrics -> Idea: Use xml to define these metrics
    time = Metric("Time (HH:MM)", "Date", 0)
    freeRam = Metric("Ram Free (MB)", "Numeric", 1)
    cpu = Metric("Cpu Usage (%)", "Numeric", 24)
    commitedRam = Metric("RAM Commited (%)", "Numeric", 25)
    metrics = [time, freeRam, cpu, commitedRam]
    # DataBase -> Idea: Use xml to define .tsv path and filename
    dataBase = DataBase(metrics)
    file = "collector-input/data-10-09.tsv"
    dataBase.setData(file)
    dataBase.fillMetrics()
    # Graphi -> Idea: Use xml or a gui to define what metrics should view (i think it'be better a gui)
    graphic = Graphic(dataBase)
    graphic.viewGraphicData(time, freeRam, shoudPlot = True, scatterColor = "red", scatterSize = 10, linewidth = 1, plotColor = "blue")
main()