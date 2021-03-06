# HighSchoolSurvey-2021

#config format
```python
MainConfig = {
    "port": 5000,
    "secret": "",
    "bypassCode": ""
}
DatabaseConfig = {
    "host": "",
    "user": "",
    "passwd": "",
    "db": "",
    "port": 3306
}

schoolCodeDict = {
    "dev": "開發測試",
    "100": "僑泰中學"
}
```
# Setup

1. `pipenv shell`
2. `pipenv install`
3. 設定 `config.py`
4. run `python app.py` (for dev)
5. run `./start.sh` (for production)

* 如果pipenv shell顯示找不到版本，請將 Pipfile 裡面的`python version`改成您的版本，需求 **>3.6**

## Frontend reCaptcha Verify

```
POST
http://server-ip:3000/auth

data = {
    "token": reCaptcha token
}

驗證失敗
401
Response:
{
    {
    "error-codes": [
        "******"
    ],
    "success": false
}

驗證成功
200
{
    "access_token": "******",
    "success": true
}
```

## Submit Data
```
POST
http://server-ip:3000/submit

header = {
    Authorization:Bearer + $JWT,
    ...other header
}

data = {
    stuId: str
    school: str
    sex: int
    grade: int
    department: str
    Q1: int
    Q2: Optional[str]
    Q3: int
    Q4: int
    Q5: int
    Q6: Optional[str]
    Q7: int
}

Response:

學校代碼錯誤
400
{
    'msg': '學校代碼錯誤', 
    'request': 'your request code'
}

重複提交
400
{
    'msg': 're-submit data'
}

成功
200
{
    'msg': 'ok'
}
```
## ToDo
1. Add GitHub Action CI
