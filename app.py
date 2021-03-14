import logging
import time

from flask import Flask, jsonify, request, send_from_directory
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required
from flask_pydantic import validate
from pymysql import NULL

from auth import generateJWTtoken, verify
from config import MainConfig, schoolCodeDict
from database import Database
from schema import frontData

#setup flask app
app = Flask(__name__)

# setup jwt
app.config["JWT_SECRET_KEY"] = MainConfig["JWTsecret"]
jwt = JWTManager(app)

#root route
#TODO sc argument not pass to index.html
@app.route("/")
def root():
    return "<script>window.location.href='index.html';</script>"
    
#homepage route
@app.route("/<path:path>")
def index(path):
    return send_from_directory('frontend', path)

# reCaptcha verify
@app.route("/auth", methods=["POST"])
def authFunction():
    #檢查傳遞資料是否正確
    if(not("token" in request.json)):
        return jsonify({
            "msg": "argument error"
        }), 400

    #驗證
    token = request.json["token"]
    verifyRes = verify(token)

    # 如果通過reCaptcha，才發給jwt token
    if(not(verifyRes["success"])):
        return jsonify(verifyRes), 401

    #產生 JWT token
    verifyRes.update({"access_token": generateJWTtoken(time.time())})
    print(verifyRes)
    return jsonify(verifyRes), 200


@app.route("/submit", methods=['POST'])
@validate()
@jwt_required()
def submit(body: frontData):
    current_user = get_jwt_identity()
    print(current_user)

    # 建立資料庫控制器
    d = Database("Main")

    # 檢查學校代碼
    schoolCode = request.json["school"]
    if(schoolCode not in schoolCodeDict):
        schoolCode = NULL

        err = {
            "msg": "學校代碼錯誤",
            "request": request.json["school"]
        }
        return jsonify(err), 400

    else:
        schoolCode = schoolCodeDict[request.json["school"]]
        print(request.json["stuId"])

    # 檢查學號是否重複，並且防止SQL注入
    result = d.checkStuId(request.json["stuId"], schoolCode)

    if(result and (request.json["stuId"] != MainConfig["bypassCode"])):
        return jsonify({
            "msg": "re-submit data"
        }), 400

    # 建立資料
    Q2 = NULL
    Q6 = NULL
    if("Q2" in request.json):
        Q2 = request.json["Q2"]

    if("Q6" in request.json):
        Q6 = request.json["Q6"]

    data = frontData(
        stuId=request.json["stuId"],
        school=schoolCode,
        sex=request.json["sex"],
        grade=request.json["grade"],
        department=request.json["department"],
        Q1=request.json["Q1"],
        Q2=Q2,
        Q3=request.json["Q3"],
        Q4=request.json["Q4"],
        Q5=request.json["Q5"],
        Q6=Q6,
        Q7=request.json["Q7"]
    )

    # 寫入資料庫
    d.insertDict(dict(data))
    d.closeDB()

    return jsonify({
        "msg": "ok"
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=MainConfig["port"])
