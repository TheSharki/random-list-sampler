from pandas_ods_reader import read_ods
from .helpers import *
from .constants import *

class Datatable:

    def __init__(self, absPathStr):
        self.__absPath = absPathStr
        self.__dataFrame = read_ods(absPathStr, 1, headers=True)
        self.__CATEGORY_HEADER = 'Category'

    def getCategories(self):
        categories = list(self.__dataFrame[self.__CATEGORY_HEADER].unique())
        # Check if element exist in List, before removing
        if None in categories:
            categories.remove(None)
        return categories

    def getEntries(self, categoryName):
        entries = self.__dataFrame[(self.__dataFrame.Category == categoryName) & (self.__dataFrame.Done.isnull())] #"Category=='{0}' & Done==None".format(category["entry"]))
        return entries

    def getEntryCount(self, categoryName):
        return len(self.getEntries(categoryName))

    def getEntry(self, categoryName, index):
        entries = self.getEntries(categoryName)
        if index < 0 or index >= len(entries):
            return None
        return entries.iloc[index]


    def count(self):
        return len(self.__dataFrame.index)

    def getOrigin(self):
        return self.__absPath
