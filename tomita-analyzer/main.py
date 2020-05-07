import json
import os
import subprocess as sub
import sys
sys.path.append("..")
from config import DATA_PATH
from model import Connection, Mongo
from dbconfig import TABLE_NAME, DATABASE_NAME

# рекурсивно обходим все подкаталоги папки дата
# загружаем с каждого json text
# для каждого из них создаем output
# создаем файлик input.txt с новым текстом
# получаем output.txt
# сохраняем его в бд)


def analyze(data: list):
    for text in data:
        with open(os.path.join(os.getcwd(), 'input.txt'), 'w') as inputFile:
            inputFile.writelines(text)
            p = sub.Popen(["tomita-parser", "config.proto"], stdout=sub.PIPE, stderr=sub.PIPE)
            out, err = p.communicate()
            print(out, err)
            with open(os.path.join(os.getcwd(), 'output.txt')) as outputFile:
                print(outputFile.readlines())


def getDataJSONs():
    data = []
    for address, dirs, files in os.walk(DATA_PATH):
        for file in files:
            if not file.endswith(".json"):
                continue
            with open(os.path.join(address, file)) as myjson:
                jsondata = json.load(myjson)
                text = jsondata['text']
                data.append(text)
    return data


def getDataDBs(mongo):
    return mongo.selectAllMongo(TABLE_NAME)



if __name__ == '__main__':
    conn = Connection().getConnection()
    mongo = Mongo(conn, DATABASE_NAME)

    data = getDataJSONs()
    #data = getDataDBs(mongo)
    analyze(data)