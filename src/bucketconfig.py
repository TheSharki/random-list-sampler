from .helpers import *
from .constants import *
from .datatable import *

class CategoryData:
    def __init__(self, categoryName, weight = 1.0):
        self.__categoryName = categoryName
        self.__weight = weight

    @classmethod
    def fromJson(cls, jsonObj):
        return cls(jsonObj["category"], jsonObj["weight"])

    def getWeight(self):
        return self.__weight

    def getCategoryName(self):
        return self.__categoryName


    def toJson(self):
        jsonObj = { }
        jsonObj["category"] = self.__categoryName
        jsonObj["weight"] = self.__weight
        return jsonObj

class Bucket:
    def __init__(self, bucketId, entries = None):
        self.__bucketId = bucketId
        if entries is None:
            entries = []
        self.__entries = entries

    @classmethod
    def fromJson(cls, jsonObj):
        id = jsonObj["id"]
        entriesJson = jsonObj["entries"]
        entries = []
        for entryJson in entriesJson:
            entry = CategoryData.fromJson(entryJson)
            entries.append(entry)
        return cls(id, entries)

    def addEntry(self, categoryName, weight = 1.0):
        self.__entries.append(CategoryData(categoryName, weight))

    def getEntries(self):
        return self.__entries

    def getTotalWeight(self):
        totalWeight = 0
        for catData in self.__entries:
            totalWeight += catData.getWeight()
        return totalWeight

    def count(self):
        return len(getEntries(self))

    def toJson(self):
        jsonObj = { }
        jsonObj["id"] = self.__bucketId
        jsonObj["entries"] = []
        for entry in self.__entries:
            jsonObj["entries"].append(entry.toJson())
        return jsonObj

    def toString(self):
        stringObj = "{0}: ".format(self.__bucketId)
        for entry in self.__entries:
            stringObj += "{0}, ".format(entry.getCategoryName())
        return stringObj

class BucketConfig:

    def __init__(self, buckets = {}):
        self.__buckets = buckets

    @classmethod
    def fromDatatable(cls, dataTable):
        loopVar = True
        while loopVar:
            bucketConfig = cls()
            for category in dataTable.getCategories():
                # print(category)
                bucketIndex = fetchNonEmptyStringInput("What bucket do you want to put the category '{0}'?".format(category))
                bucketConfig.addEntry(bucketIndex, category)
            print (">Result is:")
            print (bucketConfig.toString())
            loopVar = not showDialogue("Are you okay with this configuration? (No to regenerate)", True)
        return bucketConfig

    @classmethod
    def findOrCreateFrom(cls, dataTable):
        if not doesFileExist(BUCKET_CONFIG_PATH):
            print("Did not find file '{0}', creating new... ")
            categoryBuckets = BucketConfig.fromDatatable(dataTable)
            categoryBuckets.save(BUCKET_CONFIG_PATH)
        else:
            if showDialogue("File '{0}' detected, do you want to regenerate?".format(BUCKET_CONFIG_PATH), False):
                categoryBuckets = BucketConfig.fromDatatable(dataTable)
                categoryBuckets.save(BUCKET_CONFIG_PATH)
            else:
                print("Loading existing file '{0}'...".format(BUCKET_CONFIG_PATH))
                categoryBuckets = BucketConfig.fromFile(BUCKET_CONFIG_PATH)
        return categoryBuckets

    @classmethod
    def fromFile(cls, pathStr):
        if not doesFileExist(pathStr):
            return cls()
        bucketFileData = loadJson(pathStr)
        bucketArr = bucketFileData["content"]
        buckets = []
        for bucketData in bucketArr:
            buckets.append(Bucket.fromJson(bucketData))
        return cls(buckets)

    def count(self):
        return len(self.__buckets.keys())

    def isEmpty(self):
        return self.count() == 0

    def addEntry(self, bucketId, category, weight = 1.0):
        if bucketId not in self.__buckets:
            self.__buckets[bucketId] = Bucket(bucketId)
        self.__buckets[bucketId].addEntry(category, weight)

    def getBuckets(self):
        return list(self.__buckets)

    def save(self, pathStr):
        fileObj = {}
        fileObj["content"] = []
        for bucket in self.getBuckets():
            fileObj["content"].append(bucket.toJson())
        saveJson(fileObj, pathStr)

    def toString(self):
        data = "BucketConfig: \n"
        for bucket in self.getBuckets():
            data += "{0} \n".format(bucket.toString())
        return data
