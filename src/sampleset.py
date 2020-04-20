from .datatable import *
from .helpers import *

class SampleSet:

    def __init__(self, dataTable, samples = []):
        self.__dataTable = dataTable
        self.__data = {}
        self.__data["Answers"] = samples
        self.__data["Origin"] = self.__dataTable.getOrigin()

    @classmethod
    def fromFile(cls, path):
        jsonObj = loadJson(path)
        dataTable = Datatable(jsonObj["Origin"])
        return cls(dataTable, jsonObj["Answers"])

    def getSamples(self):
        # TODO incomplete
        return self.__data["Answers"]

    def addSample(self, sample):
        self.__data["Answers"].append(sample)

    def getOrigin(self):
        return self.__data["Origin"]

    def save(self, pathStr):
        saveJson(self.__data, pathStr)

    def toString(self):
        data = "SampleSet: \n"
        data += "Origin: {0} \n".format(str(self.getOrigin()))
        for sample in self.__data["Answers"]:
            data += "{0} \n".format(sample)
        return data
