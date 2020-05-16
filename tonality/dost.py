from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
from model import Connection, Mongo
from dbconfig import DATABASE_NAME, TABLE_NAME

messages = [
    'хорошо',
    'неочевидно',
    'зазорно'
]

def predict(words):
    results = model.predict(words, k=2)
    return results


tokenizer = RegexTokenizer()
model = FastTextSocialNetworkModel(tokenizer=tokenizer)

conn = Connection().getConnection()
mongo = Mongo(conn, DATABASE_NAME)
listOfTexts = mongo.selectAll(TABLE_NAME)

results = predict(listOfTexts)


for message, sentiment in zip(listOfTexts, results):
    print(message, '->', sentiment)