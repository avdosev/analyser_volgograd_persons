import json
import os
import subprocess as sub
import sys
sys.path.append("..")
from config import DATA_PATH
from dbmodel import Connection, Mongo
from dbconfig import TABLE_NAME, DATABASE_NAME


conn = Connection().getConnection()
mongo = Mongo(conn, DATABASE_NAME)


def getFactsById(id):
    text = [mongo.selectBy(TABLE_NAME, '_id', id)['text']]
    res = analyze(text)
    mongo.update(TABLE_NAME, id, 'sequences', res)
    return res


def analyze(data: list):  # функция должна вернуть факты и записать их в бд в sequences # но она делает не то
    for text in data:
        if os.path.split(os.getcwd())[-1] != "tomita":
            os.chdir("tomita")

        with open(os.path.join(os.getcwd(), 'input.txt'), 'w') as inputFile:
            inputFile.writelines(text)
            p = sub.Popen(["tomitaparser", "places.proto"], stdout=sub.PIPE, stderr=sub.PIPE)
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