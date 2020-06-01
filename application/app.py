from flask import Flask, render_template, json, request
from flask import jsonify, send_from_directory

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


@app.route('/getTonality/<id>')
def getTonality(id):
    from tonality.dost import  tokenizeById
    token = tokenizeById(id)
    print(token)
    return jsonify(token)





if __name__ == "__main__":
    app.run(port=5000)
