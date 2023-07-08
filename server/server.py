from flask import Flask, jsonify, request
import json
from question import *
from flask_cors import CORS
import sqlite3
import uuid

app = Flask(__name__)
CORS(app)

dbAddress = "./theBrain.db"

@app.route("/")
def test():
    return "amongus"

@app.route("/getData")
def getData():
    formUUID = request.args.get("form")
    connection = sqlite3.connect(dbAddress)
    cursor = connection.execute(f"SELECT * FROM Questions WHERE formUUID = '{formUUID}'")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify({"data": rows})
    
@app.route("/createQuestion", methods=['POST'])
def createQuestion():
    questionType = json.loads(request.data)["questionType"]
    
    newQuestion = LongFormQuestion("temp", "temp", str(uuid.uuid4()), "", questionType, "")
    
    connection = sqlite3.connect(dbAddress)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Questions (questionUUID, formUUID, userUUID, questionTitle, isRequired, questionType, placeholderText) VALUES (?, ?, ?, ?, ?, ?, ?)", (newQuestion.selfUUID, newQuestion.formUUID, newQuestion.userUUID, newQuestion.questionTitle, newQuestion.isRequired, 0, newQuestion.placeholderText))
    connection.commit()
    cursor.close()
    connection.close()
    
    return jsonify({"data": [newQuestion.selfUUID, newQuestion.formUUID, newQuestion.userUUID, newQuestion.questionTitle, newQuestion.isRequired, 0, newQuestion.placeholderText]})

@app.route("/editQuestion", methods=['POST'])
def editQuestion():
    questionData = json.loads(request.data)["data"]
    print(questionData)

    connection = sqlite3.connect(dbAddress)
    cursor = connection.cursor()
    
    cursor.execute(f"UPDATE Questions SET questionUUID = ?, formUUID = ?, userUUID = ?, questionTitle = ?, isRequired = ?, questionType = ?, placeholderText = ? WHERE questionUUID = ?", (questionData[0], questionData[1], questionData[2], questionData[3], questionData[4], questionData[5], questionData[6], questionData[0]))
    connection.commit()
    cursor.close()
    connection.close()
    
    return jsonify({200: "OK"})

@app.route("/deleteQuestion", methods=['POST'])
def deleteQuestion():
    
    questionID = json.loads(request.data)["questionID"]
    
    connection = sqlite3.connect(dbAddress)
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM Questions WHERE questionUUID = '{questionID}'")
    connection.commit()
    cursor.close()
    connection.close()
    
    formUUID = json.loads(request.data)["formID"]
    connection = sqlite3.connect(dbAddress)
    cursor = connection.execute(f"SELECT * FROM Questions WHERE formUUID = '{formUUID}'")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return jsonify({"data": rows})