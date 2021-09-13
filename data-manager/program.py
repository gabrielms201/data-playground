import numpy as np
import matplotlib.pyplot as plt


class Metric():
    def __init__(self, type, column):
        self.type = type.upper()
        self.column = column
        self.__content = []
    # --> 
    def setContent(self, data, line):
        if self.type == "NUMERIC":
            return self.__content.append(data[line][self.column].replace(",", "."))
        elif self.type == "DATE":
            return self.__content.append(data[line][self.column].replace("09/09/2021", "").strip())
    def getContent(self):
        return self.__content
    # -->   
class DataBase():
    def __init__(self):
        pass
    # --> 
    def setData(self, filename):
        file = open(filename, "r", encoding="UTF-8")
        data = [line.rstrip("\n") for line in file]
        data = [words.split("\t") for words in data]
        file.close()
        self.__data = data
    def getData(self):
        return self.__data
    # --> 
    def fillMetrics(self, metrics):
        for metric in metrics:
            for line in range(1, len(self.__data)):
                metric.setContent(self.__data, line)


def main():
    # Db
    dataBase = DataBase()
    dataBase.setData("Data.tsv")
    # Metrics
    time = Metric("Date", 0)
    free = Metric("Numeric", 1)
    cpu = Metric("Numeric", -2)
    commited = Metric("Numeric", -1)

    dataBase.fillMetrics([time, free, cpu, commited])