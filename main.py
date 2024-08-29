# uvicorn main:app --reload
# pip install firebase-admin


# ======= Import ========================
import firebase_admin
from firebase_admin import credentials, storage
import subprocess
import sys
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import json
# =======================================

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firebase/ewordz-ea3e2-firebase-adminsdk-fqu91-07418cc09c.json"

# pip 자체 업그레이드
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

# requirements.txt의 패키지 설치
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "-r", "requirements.txt"])


# ------- FireBase Connect --------------
cred = credentials.Certificate('firebase/ewordz-ea3e2-firebase-adminsdk-fqu91-07418cc09c.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'ewordz-project.appspot.com'
})

bucket = storage.bucket()

# Uploading a fixed JSON file to Firebase Storage
# blob = bucket.blob('example.json')
# blob.upload_from_filename(file_path)

# ---------------------------------------


# ------- FastAPI Application Create ----
app = FastAPI()
# ---------------------------------------


# ======= Functions =====================
def Load_Json(filePath):
    with open(f"{filePath}", "r") as f:
        return json.load(f)

def Read_File(filePath):
    with open(f"{filePath}", "r") as f:
        data = f.read()
        return data
    
def Dump_Json(filePath, data):
    with open(f"{filePath}", "w") as f:
        json.dump(data, f, indent=4)

def Download_Of_Firebase(filePath):
    blob = bucket.blob(f'{filePath}')
    blob.download_to_filename(filePath)
    data = Read_File(filePath)
    print(data)

def Upload_To_Firebase(filePath):
    blob = bucket.blob(f'{filePath}')
    blob.upload_from_filename(filePath)


# =======================================

# ======== Main =========================
userDataFile = "userData.json"
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def read_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/login_submit", response_class=HTMLResponse)
async def submit_form(request: Request, id: str = Form(...), pw: str = Form(...)):    
    userData = Load_Json(userDataFile)
    # 아이디가 존재하지 않는 경우 처리 추가
    try:
        if userData[f"{id}"]["pw"] == pw:
            print("로그인 성공")
            return templates.TemplateResponse("main.html", {"request": request, "userId": f"{id}", "userPw" : f"{pw}"})
        else:
            print("존재하지 않는 아이디 또는 비밀번호 틀림")
            return templates.TemplateResponse("login.html", {"request": request, "warring": "잘못된 비밀번호 또는 존재하지 않는 아이디입니다."})
    except:
        print("존재하지 않는 아이디 또는 비밀번호 틀림")
        return templates.TemplateResponse("login.html", {"request": request, "warring": "잘못된 비밀번호 또는 존재하지 않는 아이디입니다."})

@app.post("/signup_submit", response_class=HTMLResponse)
async def submit_form(request: Request, id: str = Form(...), pw: str = Form(...), pw2: str = Form(...)):   
    userData = Load_Json(userDataFile)
    if id not in userData:
        if pw == pw2:
            userData[f"{id}"] = {"pw" : f"{pw}"}
            Dump_Json(userDataFile, userData)
            Upload_To_Firebase(userDataFile)
            Download_Of_Firebase(userDataFile)
            print(f"\n[ Server Message ]\n유저 한 명이 회원가입을 성공하였습니다.\n아이디 - {id}\n[ END ]\n")
        else:
            print(f"\n[ Server Message ]\n유저 한 명이 회원가입을 실패하였습니다.\n사유 - 비밀번호가 일치하지 않습니다.\n[ END ]\n")
            return templates.TemplateResponse("signup.html", {"request": request, "warring": "비밀번호가 일치하지 않습니다."})
            
    else:
        print(f"\n[ Server Message ]\n유저 한 명이 회원가입을 실패하였습니다.\n사유 - 이미 존재하는 아이디입니다. ({id})\n[ END ]\n")
        return templates.TemplateResponse("signup.html", {"request": request, "warring": "이미 존재하는 아이디입니다."})
    
# =======================================
