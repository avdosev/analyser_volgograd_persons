from motor.motor_asyncio import AsyncIOMotorClient

# TODO: make async model

uri = "mongodb://dev:dev@localhost:27017/mydatabase?authSource=admin"
client = AsyncIOMotorClient(uri)