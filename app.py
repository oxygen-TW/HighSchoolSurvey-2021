from flask import Flask, request, Response, send_from_directory
from flask import render_template
from pymysql import NULL
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import time

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
    res = request.values.get('token')
    verifyRes = verify(res)
    
    #如果通過reCaptcha，發給jwt token
    if(verifyRes["success"]):
        return "<script>alert('請完成 recaptcha 人機驗證');history.back();</script>"
    
    return generateJWTtoken(time.time())

@app.route("/submit", methods=['POST'])
@jwt_required()
def submit():
    current_user = get_jwt_identity()
    print(current_user)
    # 建立資料庫控制器
    d = Database("Main")

    # 檢查學校代碼
    schoolCode = request.values.get('schoolCode')
    if(schoolCode not in schoolCodeDict):
        schoolCode = NULL
        return "<h1>學校代碼錯誤</h1><br>請聯絡開發人員 code=" + request.values.get('schoolCode')
    else:
        schoolCode = schoolCodeDict[request.values.get('schoolCode')]
        print(request.values.get('stuId'))

    # 檢查學號是否重複，並且防止SQL注入
    result = d.checkStuId(request.values.get('stuId'), schoolCode)

    if(result and (request.values.get('stuId') != MainConfig["bypassCode"])):
        return "<h1>感謝您，已經填寫過囉~</h1>"

    # 建立資料
    data = {
        "stuId": request.values.get('stuId'),
        "school": schoolCode,
        "sex": request.values.get('sex'),
        "grade": request.values.get('grade'),
        "department": request.values.get('dept'),
        "Q1": request.values.get('Q1'),
        "Q2": request.values.get('Q2'),
        "Q3": request.values.get('Q3'),
        "Q4": request.values.get('Q4'),
        "Q5": request.values.get('Q5'),
        "Q6": request.values.get('Q6'),
        "Q7": request.values.get('Q7'),
    }

    # 寫入資料庫
    d.insertDict(data)
    d.closeDB()

    return "<h1>感謝您的填寫!</h1>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=MainConfig["port"])
