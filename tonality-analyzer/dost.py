import sys
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
from dbmodel import Connection, Mongo
from dbconfig import DATABASE_NAME, TABLE_NAME

messages = ["да", "нет"]  # testData


def predict(words):
    return model.predict(words, k=2)


def analyze(text: list):
    # countSum = {'count': 0, 'sum': 0}
    articleTonality = {'positive': {'count': 0, 'sum': 0},
                       'negative': {'count': 0, 'sum': 0},
                       'neutral': {'count': 0, 'sum': 0},
                       'skip': {'count': 0, 'sum': 0}
                       }
    results = predict(text)
    for message, sentiment in zip(text, results):
        for tonality in articleTonality:
            if tonality in sentiment:
                if sentiment[tonality] > 0.5:
                    articleTonality[tonality]['count'] += 1

    if articleTonality['positive']['count'] > articleTonality['negative']['count']:
        return 'Negative'
    else:
        return 'Positive'



tokenizer = RegexTokenizer()
model = FastTextSocialNetworkModel(tokenizer=tokenizer)

conn = Connection().getConnection()
mongo = Mongo(conn, DATABASE_NAME)
allTable = mongo.selectAll(TABLE_NAME)
onlyText = [i['text'].split(" ") for i in allTable]




for text in onlyText:
    print(analyze(text))
