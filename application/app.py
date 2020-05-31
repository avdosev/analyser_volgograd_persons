from flask import Flask, render_template, json, request
import sys
sys.path.append("..")
from dbconfig import TABLE_NAME, DATABASE_NAME
from dbmodel import Connection, Mongo


app = Flask(__name__)
conn = Connection().getConnection()
mongo = Mongo(conn, DATABASE_NAME)


@app.route('/')
def main():
    articles = mongo.selectAll(TABLE_NAME)
    return render_template('index.html', articles=articles)




if __name__ == "__main__":
    app.run(port=5000)
