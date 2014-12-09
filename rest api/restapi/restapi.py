from flask import request, url_for, g, jsonify
from flask.ext.api import FlaskAPI, status, exceptions
import os
import sqlite3

DATABASE = 'test.db'

app = FlaskAPI(__name__)

def connect_db():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

def get_connection():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._db = connect_db()
    return db

def init_db():
    with app.app_context():
        db = get_connection()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

init_db()

def _get_all_words(one=False):
    sql = "select word, count from words"
    db = get_connection()
    cur = db.execute(sql)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def _get_word(word, one=True):
    sql = "SELECT * from words where word='%s' limit 1" %(word)
    db = get_connection()
    cur = db.execute(sql)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def _insert_word(word):
    sql = "INSERT into words values ('%s', 1)"%(word)
    db = get_connection()
    res = db.execute(sql)
    db.commit()

def _update_word(word, existing_value):
    existing_count = existing_value
    new_value = existing_count + 1
    sql = "UPDATE words set count='%s' where word='%s'"%(new_value, word)
    db = get_connection()
    rv = db.execute(sql)    
    db.commit()

def _add_word(word):
    exists = _get_word(word)
    if [] == exists or exists == None:
        _insert_word(word)
    else:
        _update_word(word, exists['count'])

@app.route("/words", methods=['GET'])
def words_list():
    words = _get_all_words()
    output = {}
    for item in words:
        output[item['word']] = item['count']
    return output

@app.route("/words/<key>", methods=['GET'])
def find_word(key):
    result = _get_word(key)
    if [] == result or result == None:
        return jsonify(key=0)
    else:
        return jsonify(key=result['count'])

@app.route("/word/<key>", methods=["PUT", "POST"])
def create_word(key):
    if ' ' in request.data['word']:
        return {"ERROR": "Failed it must be one word"}, status.HTTP_400_BAD_REQUEST
    if request.data['word'] != key:
        return {"ERROR": "Word and data mismatch"}, status.HTTP_400_BAD_REQUEST
    _add_word(key)
    return '', status.HTTP_204_NO_CONTENT

if __name__ == "__main__":
    app.run(debug=True)
