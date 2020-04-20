from pathlib import Path
import json

def doesFileExist(path):
    my_file = Path(path)
    return my_file.is_file()

def getAbsolutePath(pathStr):
    my_file = Path(pathStr)
    return my_file.absolute()

def showDialogue(question, defaultTrue):
    if (defaultTrue):
        ext = " [Y/n]"
    else:
        ext = " [y/N]"
    fullText = ">" + question + ext
    answer = input(fullText)
    if len(answer) == 0:
        return defaultTrue

    if answer[0].lower() == 'y':
        return True
    else:
        return False

def fetchNonEmptyStringInput(question):
    while True:
        answer = input(question)
        if answer and not answer.isspace():
            break
    return answer

def saveJson(jsonObj, path):
    jsonFile = json.dumps(jsonObj)
    f = open(path, "w")
    f.write(jsonFile)
    f.close()

def loadJson(path):
    with open(path) as f_in:
        jsonObj = (json.load(f_in))
    return jsonObj
