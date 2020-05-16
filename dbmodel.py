from pymongo import MongoClient

# from motor.motor_asyncio import AsyncIOMotorClient
# # TODO: make async model | Нет.
# #uri = "mongodb://dev:dev@localhost:27017/mydatabase?authSource=admin"
# client = AsyncIOMotorClient(uri)


class Connection:
    uri = None
    conn = None

    def __init__(self, host="localhost", port="27017"):
        self.uri = f"mongodb://{host}:{port}"
        self.conn = MongoClient(self.uri)  # можно и не передавать, тут по умолчанию эти данные

    def getConnection(self):
        return self.conn


class Mongo:
    mydb = None

    def __init__(self, connection, databaseName):
        self.mydb = connection[databaseName]

    def insert(self, tableName: str, data):
        mycol = self.mydb[tableName]
        insertedId = mycol.insert_many(data)
        return insertedId

    def selectAll(self, tableName: str):
        mycol = self.mydb[tableName]
        return list(mycol.find({}))

