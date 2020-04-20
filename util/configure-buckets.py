from pandas_ods_reader import read_ods
import argparse

# Argument parsing
parser = argparse.ArgumentParser(description='Parse your list.')
parser.add_argument('inputPath', help='File to load for categories')
args = parser.parse_args()

path = args.inputPath

print("Parsing file '{0}'...".format(path))

# load a file that does not contain a header row
# if no columns are provided, they will be numbered
df = read_ods(path, 1, headers=True)
createBucketFile(df)
