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
    res  = normalizeOutput(res)
    mongo.update(TABLE_NAME, id, 'sequences', res)
    return res


def normalizeOutput(array: list):
    persons = []
    places = []
    for object in array:
        if (object == "Person"):
            personInsert = True
        elif object == "{": continue
        elif object == "}":
            placeInsert = False
            personInsert = False
        elif (object == "Place"):
            placeInsert = True
        else:
            leftSide, rightSide = object.split(" = ")
            fact = {leftSide: rightSide}
            if (personInsert): persons.append(fact)
            elif placeInsert: places.append(fact)
    return {'Persons': persons, "Places": places}

    # {name: %realName%}


def analyze(data: list):  # функция должна вернуть факты и записать их в бд в sequences # но она делает не то
    for text in data:
        if os.path.split(os.getcwd())[-1] != "tomita":
            os.chdir("tomita")

        with open(os.path.join(os.getcwd(), 'input.txt'), 'w', encoding='utf-8') as inputFile:
            inputFile.writelines(text)

        p = sub.Popen(["tomitaparser", "persons.proto"], stdout=sub.PIPE, stderr=sub.PIPE)
        out, err = p.communicate()
        print(out, err)
        output = []
        with open(os.path.join(os.getcwd(), 'output.txt'), 'r', encoding='utf-8') as outputFile:
            readedNews = outputFile.readlines()
            appending = False
            for news in readedNews:

                if "Person" in news or "Place" in news:
                    appending = True
                if appending:
                    output.append(news.strip())
                if "}" in news:
                    appending = False
        return output





def getDataJSONs():
    data = []
    for address, dirs, files in os.walk('.'):
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