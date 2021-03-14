from flask import Flask, request, Response, send_from_directory
from flask import render_template
from flask import jsonify
from pymysql import NULL
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import time

import requests

from database import Database
from config import schoolCodeDict, MainConfig
from auth import verify, generateJWTtoken

app = Flask(__name__)

#setup jwt
app.config["JWT_SECRET_KEY"] = MainConfig["JWTsecret"]
jwt = JWTManager(app)

@app.route("/<path:path>")
def hello(path):
    return send_from_directory('frontend', path)

#reCaptcha verify
@app.route("/auth", methods=["POST"])
def authFunction():
    token = request.json["token"]
    verifyRes = verify(token)
    
    #如果通過reCaptcha，才發給jwt token
    if(not verifyRes["success"]):
        return jsonify(verifyRes), 401
    
    verifyRes.update({"access_token":generateJWTtoken(time.time())})
    print(verifyRes)
    return jsonify(verifyRes), 200

@app.route("/submit", methods=['POST'])
@jwt_required()
def submit():
    current_user = get_jwt_identity()
    print(current_user)
    # 建立資料庫控制器
    d = Database("Main")

    # 檢查學校代碼
    schoolCode = request.json["schoolCode"]
    if(schoolCode not in schoolCodeDict):
        schoolCode = NULL

        err = {
            "msg":"學校代碼錯誤",
            "request": request.json["schoolCode"]
        }
        return jsonify(str(err)), 400

    else:
        schoolCode = schoolCodeDict[request.json["schoolCode"]]
        print(request.json["stuId"])

    # 檢查學號是否重複，並且防止SQL注入
    result = d.checkStuId(request.json["stuId"], schoolCode)
    print(result)
    if(result and (request.json["stuId"] != MainConfig["bypassCode"])):
        return jsonify(str({
            "msg": "re-submit data"
        })), 400

    # 建立資料
    data = {
        "stuId": request.json["stuId"],
        "school": schoolCode,
        "sex": request.json["sex"],
        "grade": request.json["grade"],
        "department": request.json["dept"],
        "Q1": request.json["Q1"],
        "Q2": request.json["Q2"],
        "Q3": request.json["Q3"],
        "Q4": request.json["Q4"],
        "Q5": request.json["Q5"],
        "Q6": request.json["Q6"],
        "Q7": request.json["Q7"],
    }

    # 寫入資料庫
    d.insertDict(data)
    d.closeDB()

    return jsonify(str({
        "msg": "ok"
    })), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=MainConfig["port"])
