from flask import Flask, jsonify, request
import json
from question import *
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

@app.route("/")
def test():
    return "amongus"

@app.route("/createQuestion", methods=['POST'])
def createQuestion():
    questionIn = json.loads(request.data)
    print(questionIn)
    questionIn = Question(questionIn["userUUID"], questionIn["formUUID"], questionIn["selfUUID"], questionIn["questionTitle"], questionIn["isRequired"])
    
    connection = sqlite3.connect("./server/theBrain.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Questions (questionUUID, formUUID, userUUID, questionTitle, isRequired, questionType) VALUES (?, ?, ?, ?, ?, ?)", (questionIn.selfUUID, questionIn.formUUID, questionIn.userUUID, questionIn.questionTitle, questionIn.isRequired, 0))
    connection.commit()
    cursor.close()
    connection.close()
    
    return jsonify({'200':'OK'})