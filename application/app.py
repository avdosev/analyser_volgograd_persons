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


@app.route('/getTonality/<id>')
def getTonality(id):
    print(id)
    import subprocess as sub
    p = sub.Popen(["python", "tonality-analyzer", "dost.py", "--id", id], stdout=sub.PIPE, stderr=sub.PIPE)
    out, err = p.communicate()
    print(out)
    print(err)




if __name__ == "__main__":
    app.run(port=5000)
