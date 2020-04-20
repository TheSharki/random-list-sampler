from .datatable import *
from .bucketconfig import *
from .sampleset import *
import random

def getSampleIndex(dataTable, bucket):
    totalWeight = bucket.getTotalWeight()

    totalCount = 0
    randomIndex = random.random();
    curWeight = 0
    # print ("Random seed: {0}".format(randomIndex))
    for catData in bucket.getEntries():
        categoryName = catData.getCategoryName()
        catWeight = catData.getWeight()
        if ((curWeight + catWeight) / totalWeight) >= randomIndex:
            randomTaskIndex = (randomIndex - (curWeight / totalWeight)) / (catWeight / totalWeight)
            index = int(randomTaskIndex * (dataTable.getEntryCount(categoryName) - 1))
            return categoryName, index
        else:
            curWeight += catWeight

    # We should never reach here
    #print ("ERROR: Something went wrong...")
    firstCat = bucket.getEntries()[0]
    categoryName = firstCat.getCategoryName()
    return categoryName, 0

def sampleEachBucket(dataTable, bucketConfig):
    sampleSet = SampleSet(dataTable)
    for bucket in bucketConfig.getBuckets():
        sampleCategory, sampleIndex = getSampleIndex(dataTable, bucket)
        sample = dataTable.getEntry(sampleCategory, sampleIndex)
        sampleSet.addSample(sample)
        # print ("Selected random choice for category: {0}".format(answer["Name"]))

    return sampleSet
