import sys
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
from dbmodel import Connection, Mongo
from dbconfig import DATABASE_NAME, TABLE_NAME


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

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--id', action='store', dest='id', help='Id записи в базы данных')
parser.add_argument('--text', action='store', dest='text', help='Текст, который нужно анализировать')

args = parser.parse_args()
print(args)

if args.id:
    allTable = mongo.selectBy(TABLE_NAME, '_id', args.id)
    print(allTable)
    # onlyText = [i['text'].split(" ") for i in allTable]
    # for text in onlyText:
    #     print(analyze(text))
elif args.text:
    allTable = mongo.selectBy(TABLE_NAME, 'text', args.text)
