import sys
import os.path
import argparse

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
from dbmodel import Connection, Mongo
from dbconfig import DATABASE_NAME, TABLE_NAME


def tokenizeById(id):
    row = mongo.selectBy(TABLE_NAME, '_id', id)
    text = [row['text']]
    res = analyze(text)
    print(res)
    mongo.update(TABLE_NAME, id, 'tonality', res)
    return res


def tokenizeByText(text: str):
    messages = [text]
    res = analyze(messages)
    print(res)
    return res


def predict(words):
    return model.predict(words, k=4)


def analyze(text: list):
    results = predict(text)
    return results[0]


tokenizer = RegexTokenizer()
model = FastTextSocialNetworkModel(tokenizer=tokenizer)

conn = Connection().getConnection()
mongo = Mongo(conn, DATABASE_NAME)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', action='store', dest='id', help='Id записи в базы данных')
    parser.add_argument('--text', action='store', dest='text', help='Текст, который нужно анализировать')
    args = parser.parse_args()
    print(args)

    if args.id:
        tokenizeById(args.id)
    elif args.text:
        tokenizeByText(args.text)
    else:
        print("Аргументы не предоставлены.")