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

@app.route("/getFormInfo")
def getFormInfo():
    formUUID = request.args.get("form")
    connection = sqlite3.connect(dbAddress)
    cursor = connection.execute(f"SELECT formTitle, formDescription, userUUID FROM Forms WHERE formUUID = '{formUUID}'")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify({"data": rows})    
    
@app.route("/createQuestion", methods=['POST'])
def createQuestion():
    formUUID = json.loads(request.data)["formUUID"]
    questionType = json.loads(request.data)["questionType"]
    connection = sqlite3.connect(dbAddress)
    cursor = connection.cursor()
    cursor.execute(f"SELECT userUUID FROM Forms WHERE formUUID = ?", [formUUID])
    userUUID = cursor.fetchall()[0][0]
    newQuestion = LongFormQuestion(userUUID, formUUID, str(uuid.uuid4()), "", questionType, "")
    
    
    cursor.execute("INSERT INTO Questions (questionUUID, formUUID, userUUID, questionTitle, isRequired, questionType, placeholderText) VALUES (?, ?, ?, ?, ?, ?, ?)", (newQuestion.selfUUID, newQuestion.formUUID, newQuestion.userUUID, newQuestion.questionTitle, newQuestion.isRequired, 0, newQuestion.placeholderText))
    connection.commit()
    cursor.close()
    connection.close()
    
    return jsonify({"data": [newQuestion.selfUUID, newQuestion.formUUID, newQuestion.userUUID, newQuestion.questionTitle, newQuestion.isRequired, 0, newQuestion.placeholderText]})

@app.route("/editQuestion", methods=['POST'])
def editQuestion():
    questionData = json.loads(request.data)["data"]

    connection = sqlite3.connect(dbAddress)
    cursor = connection.cursor()
    
    cursor.execute(f"UPDATE Questions SET questionUUID = ?, formUUID = ?, userUUID = ?, questionTitle = ?, isRequired = ?, questionType = ?, placeholderText = ? WHERE questionUUID = ?", (questionData[0], questionData[1], questionData[2], questionData[3], questionData[4], questionData[5], questionData[6], questionData[0]))
    connection.commit()
    cursor.close()
    connection.close()
    
    return jsonify({200: "OK"})

@app.route("/editFormInfo", methods=['POST'])
def editFormInfo():
    formInfoData = json.loads(request.data)["data"]
    
    connection = sqlite3.connect(dbAddress)
    cursor = connection.cursor()
    
    cursor.execute(f"UPDATE Forms SET formTitle = ?, formDescription = ? WHERE formUUID = ?", (formInfoData[0], formInfoData[1], formInfoData[2]))
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

@app.route("/getForm", methods=['POST'])
def getForm():
    
    userID = json.loads(request.data)["userID"]
    
    connection = sqlite3.connect(dbAddress)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM Forms WHERE userUUID = '{userID}'")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return jsonify({"data": rows})

@app.route("/getUsername", methods=['POST'])
def getUsername():
    
    userID = json.loads(request.data)["userID"]
    connection = sqlite3.connect(dbAddress)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM Users WHERE userUUID = '{userID}'")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify({"data": rows})

@app.route("/submitResponse", methods=['POST'])
def submitResponse():
    responses = json.loads(request.data)["data"]
    connection = sqlite3.connect(dbAddress)
    cursor = connection.cursor()
    for response in responses:
        cursor.execute("INSERT INTO Responses (responseUUID, formUUID, questionUUID, response) VALUES (?, ?, ?, ?)", (response[0], response[1], response[2], response[3]))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({200: "OK"})

@app.route("/newForm", methods=['POST'])
def newsForm():
    response = json.loads(request.data)["data"]
    connection = sqlite3.connect(dbAddress)
    cursor = connection.cursor()
    print(response[1])
    cursor.execute("INSERT INTO Forms (formUUID, userUUID, formTitle, dateCreated, formDescription) VALUES (?, ?, ?, ?, ?)", (response[0], response[1], response[2], response[3], response[4]))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({200: "OK"})

@app.route("/signUp", methods=['POST'])
def signUp():
    response = json.loads(request.data)["data"]
    connection = sqlite3.connect(dbAddress)
    cursor = connection.cursor()
    
    cursor.execute(f"SELECT * FROM Users WHERE username = '{response[0]}'")
    rows = cursor.fetchall()

    if rows == []:    
        newUUID = uuid.uuid4()
        cursor.execute("INSERT INTO Authentication VALUES (?, ?)", (str(newUUID), response[1]))
        cursor.execute("INSERT INTO Users VALUES(?, ?)", (str(newUUID), response[0]))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({200: "OK"})
    else:
        return jsonify({"Error": "That Username is Already Taken"})
    
@app.route("/login", methods=['POST'])
def login():
    response = json.loads(request.data)["data"]
    connection = sqlite3.connect(dbAddress)
    cursor = connection.cursor()
    
    cursor.execute(f"SELECT * FROM Users WHERE username = '{response[0]}'")
    try:
        userUUID = cursor.fetchall()[0][0]
    except:
        userUUID = []
    print(userUUID)

    if userUUID == []:    
        return jsonify({"Error": "That Username does not Exist"})
    else:
        cursor.execute(f"SELECT * FROM Authentication WHERE userUUID = '{userUUID}'")
        password = cursor.fetchall()[0][1]
        if response[1] != password:
            return jsonify({"Error": "Incorrect Password"})
    return jsonify({"uuid": userUUID}) 