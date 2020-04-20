import argparse
import src.constants
from src.helpers import *
import src.datatable
import src.bucketconfig
from src.sampler import *

# Argument parsing
parser = argparse.ArgumentParser(description='Parse your list.')
parser.add_argument('inputPath', help='Inputfile containing the samples')
parser.add_argument('--cacheless', help='Prevent the script from caching the sample result.', action="store_true")
args = parser.parse_args()

path = args.inputPath
absolutePath = str(getAbsolutePath(path))

print ("========================= Reading file (1/3) =========================")

dataTable = Datatable(absolutePath)

print ("========================= Checking category setup (2/3) =========================")

categoryBuckets = BucketConfig.findOrCreateFrom(dataTable);

print ("========================= Checking randomized selections (3/3) =========================")

def tryLoadSampleSet():
    if doesFileExist(SELECTION_CACHE_PATH):
        currentRandomSelection = SampleSet.fromFile(SELECTION_CACHE_PATH)
        if currentRandomSelection.getOrigin() == absolutePath:
            if not showDialogue("File '{0}' detected, do you want to regenerate?".format(SELECTION_CACHE_PATH), False):
                print ("Reading file {0}...".format(SELECTION_CACHE_PATH))
                jsonObj = loadJson(SELECTION_CACHE_PATH)
                for catId in jsonObj["Answers"]:
                    print("Generated answer {0}".format(jsonObj["Answers"][catId]))
                return True
        else:
            if not showDialogue("File '{0}' detected from other source {1}, do you want to overwrite?".format(SELECTION_CACHE_PATH, currentRandomSelection["Origin"]), False):
                print ("Exiting...")
                return True
    return False

if args.cacheless or not tryLoadSampleSet():
    sampleSet = sampleEachBucket(dataTable, categoryBuckets)
    print (sampleSet.toString())
    if not args.cacheless:
        sampleSet.save(SELECTION_CACHE_PATH)



# Pandas DataFrame
# print(df["Name"])

# print (df.query('Category==10'))
