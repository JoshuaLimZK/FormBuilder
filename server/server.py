from flask import Flask, jsonify, request
import json
from question import *
from flask_cors import CORS
import sqlite3
import uuid

app = Flask(__name__)
CORS(app)

@app.route("/")
def test():
    return "amongus"

@app.route("/getData")
def getData():
    formUUID = request.args.get("form")
    connection = sqlite3.connect("./server/theBrain.db")
    cursor = connection.execute(f"SELECT * FROM Questions WHERE formUUID = '{formUUID}'")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify({"data": rows})
    
    
    return jsonify({})

@app.route("/createQuestion", methods=['POST'])
def createQuestion():
    questionType = json.loads(request.data)["questionType"]
    
    newQuestion = LongFormQuestion("temp", "temp", str(uuid.uuid4()), "", questionType)
    
    connection = sqlite3.connect("./server/theBrain.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Questions (questionUUID, formUUID, userUUID, questionTitle, isRequired, questionType) VALUES (?, ?, ?, ?, ?, ?)", (newQuestion.selfUUID, newQuestion.formUUID, newQuestion.userUUID, newQuestion.questionTitle, newQuestion.isRequired, 0))
    connection.commit()
    cursor.close()
    connection.close()
    
    return jsonify({"data": [newQuestion.selfUUID, newQuestion.formUUID, newQuestion.userUUID, newQuestion.questionTitle, newQuestion.isRequired, 0]})

@app.route("/deleteQuestion", methods=['POST'])
def deleteQuestion():
    
    questionID = json.loads(request.data)["questionID"]
    
    connection = sqlite3.connect("./server/theBrain.db")
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM Questions WHERE questionUUID = '{questionID}'")
    connection.commit()
    cursor.close()
    connection.close()
    
    formUUID = json.loads(request.data)["formID"]
    connection = sqlite3.connect("./server/theBrain.db")
    cursor = connection.execute(f"SELECT * FROM Questions WHERE formUUID = '{formUUID}'")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return jsonify({"data": rows})