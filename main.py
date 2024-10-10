# uvicorn main:app --reload
# pip install firebase-admin


# ======= Import ========================
import firebase_admin
from firebase_admin import credentials, storage
from random import shuffle
import subprocess
import sys
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import hashlib
import os
import json
from datetime import date
from starlette.middleware.sessions import SessionMiddleware
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

app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
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

def Hashing(data):
    hashedData = hashlib.sha256()
    hashedData.update(f"{data}".encode("utf-8"))
    return hashedData.hexdigest()

def Get_Stage():
    stage_list = []
    for i in range(1, 31):
        stage_list.append(i)
    
    shuffle(stage_list)
    return stage_list
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
        if userData[f"{id}"]["pw"] == Hashing(pw):
            print("로그인 성공")
            request.session['user_id'] = id
            return RedirectResponse(url="/main")
        else:
            print("존재하지 않는 아이디 또는 비밀번호 틀림")
            return templates.TemplateResponse("login.html", {"request": request, "warning": "잘못된 비밀번호 또는 존재하지 않는 아이디입니다."})
    except:
        print("존재하지 않는 아이디 또는 비밀번호 틀림")
        return templates.TemplateResponse("login.html", {"request": request, "warning": "잘못된 비밀번호 또는 존재하지 않는 아이디입니다."})

@app.get("/aaa", response_class=HTMLResponse)
async def aaa(request: Request):
    return templates.TemplateResponse("signupSuccess.html", {"request": request})

@app.post("/signup_submit", response_class=HTMLResponse)
async def submit_form(request: Request, id: str = Form(...), pw: str = Form(...), pw2: str = Form(...), name: str = Form(...)):   
    pw = Hashing(pw)
    pw2 = Hashing(pw2)
    userData = Load_Json(userDataFile)
    if id not in userData:
        if pw == pw2:
            stage = Get_Stage()
            print(stage)
            userData[f"{id}"] = {
                "pw" : f"{pw}",
                "name" : f"{name}",
                "character": "ruby",
                "attendance": [0, 0, 0, 0, 0, 0, 0],
                "sequence": 0,
                "stage": stage,
                "now_stage_idx": 0,
                "point": 0,
                "now_rate" : 0,
                "best_rate" : 0,
                "d_study_count": 0,
                "total_study_count": 0,
                "total_try_count": 0,
                "total_wrong_count": 0
            }
            Dump_Json(userDataFile, userData)
            Upload_To_Firebase(userDataFile)
            Download_Of_Firebase(userDataFile)
            time = date.today()
            print(f"\n[ Server Message ]\n유저 한 명이 회원가입을 성공하였습니다.\n아이디 - {id}\n[ END ]\n")
            return templates.TemplateResponse("signupSuccess.html", {"request": request, "id" : id, "time" : time})
        else:
            print(f"\n[ Server Message ]\n유저 한 명이 회원가입을 실패하였습니다.\n사유 - 비밀번호가 일치하지 않습니다.\n[ END ]\n")
            return templates.TemplateResponse("signup.html", {"request": request, "warning": "비밀번호가 일치하지 않습니다."})
            
    else:
        print(f"\n[ Server Message ]\n유저 한 명이 회원가입을 실패하였습니다.\n사유 - 이미 존재하는 아이디입니다. ({id})\n[ END ]\n")
        return templates.TemplateResponse("signup.html", {"request": request, "warning": "이미 존재하는 아이디입니다."})

@app.post ("/character", response_class=HTMLResponse)
async def character(request: Request, character: str=Form(...)):
    id = request.session.get('user_id')
    userData = Load_Json(userDataFile)
    if character is not None:
        userData[id]["character"] = character
    else:
        userData[id]["character"] = "ruby"  # 기본값 설정
    Dump_Json(userDataFile, userData)
    print(character)

    return RedirectResponse(url="/main")

@app.post ("/main", response_class=HTMLResponse)
async def read_main(request: Request):
    id = request.session.get('user_id')
    # to_date = date.today().weekday()
    # if to_date == 6:
    #     w_study_count = 0
    #     w_wrong_count = 0
    #     d_study_count = 0
    #     now_rate = 0
                
    userData = Load_Json(userDataFile)
    name = userData[f"{id}"]["name"]
    point = userData[f"{id}"]["point"]
    best_rate = userData[f"{id}"]["best_rate"]
    now_rate = userData[f"{id}"]["now_rate"]
    attendance_check = userData[f"{id}"]["attendance"]
    sequence = userData[f"{id}"]["sequence"]
    d_study_count = userData[f"{id}"]["d_study_count"]
    total_study_count = userData[f"{id}"]["total_study_count"]
    total_try_count = userData[f"{id}"]["total_try_count"]
    total_wrong_count = userData[f"{id}"]["total_wrong_count"]
    character = userData[f"{id}"]["character"]
    
    # 정답률 구하기
    if total_try_count != 0:
        now_rate = ( total_try_count - float(total_wrong_count) ) / total_try_count * 100.0
        now_rate = round(now_rate, 1)
        best_rate = round(best_rate, 1)
        if now_rate > best_rate: best_rate = now_rate

        userData[f"{id}"]["now_rate"] = now_rate
        userData[f"{id}"]["best_rate"] = best_rate
        Dump_Json(userDataFile, userData)
    return templates.TemplateResponse("main.html", {
        "request": request,
        "sequence": sequence,
        "character": character,
        "user_id": id,
        "user_name": name,
        "user_point" : point,
        "user_best_rate": best_rate,
        "user_now_rate" : now_rate,
        "attendance": attendance_check,
        "d_study_count": d_study_count,
        "total_study_count": total_study_count,
        "total_try_count": total_try_count,
        "total_wrong_count": total_wrong_count
        })

@app.get ("/main", response_class=HTMLResponse)
async def read_main_get(request: Request):
    id = request.session.get('user_id')
    # to_date = date.today().weekday()
    # if to_date == 6:
    #     w_study_count = 0
    #     w_wrong_count = 0
    #     d_study_count = 0
    #     now_rate = 0
                
    userData = Load_Json(userDataFile)
    name = userData[f"{id}"]["name"]
    point = userData[f"{id}"]["point"]
    best_rate = userData[f"{id}"]["best_rate"]
    now_rate = userData[f"{id}"]["now_rate"]
    attendance_check = userData[f"{id}"]["attendance"]
    sequence = userData[f"{id}"]["sequence"]
    d_study_count = userData[f"{id}"]["d_study_count"]
    total_study_count = userData[f"{id}"]["total_study_count"]
    total_try_count = userData[f"{id}"]["total_try_count"]
    total_wrong_count = userData[f"{id}"]["total_wrong_count"]
    character = userData[f"{id}"]["character"]
    
    # 정답률 구하기
    if total_try_count != 0:
        now_rate = ( total_try_count - float(total_wrong_count) ) / total_try_count * 100.0
        now_rate = round(now_rate, 1)
        best_rate = round(best_rate, 1)
        if now_rate > best_rate: best_rate = now_rate

        userData[f"{id}"]["now_rate"] = now_rate
        userData[f"{id}"]["best_rate"] = best_rate
        Dump_Json(userDataFile, userData)
    return templates.TemplateResponse("main.html", {
        "request": request,
        "sequence": sequence,
        "user_id": id,
        "user_name": name,
        "character": character,
        "user_point" : point,
        "user_best_rate": best_rate,
        "user_now_rate" : now_rate,
        "attendance": attendance_check,
        "d_study_count": d_study_count,
        "total_study_count": total_study_count,
        "total_try_count": total_try_count,
        "total_wrong_count": total_wrong_count
        })

@app.post("/attendance", response_class=HTMLResponse)
async def attendance(request: Request, id: str = Form(...), day: int = Form(...)):
    userData = Load_Json(userDataFile)
    
    today_date = date.today()

    last_attendance_date = userData[f"{id}"].get("last_attendance_date")

    if last_attendance_date == str(today_date):
        return JSONResponse(content={"message": "이미 출석 체크를 하셨습니다."}, status_code=400)

    # 출석 체크 로직
    userData[f"{id}"]["attendance"][day] = 1  # 출석 체크
    userData[f"{id}"]["sequence"] += 1
    sequence = userData[f"{id}"]["sequence"]

    Dump_Json(userDataFile, userData)
    return templates.TemplateResponse("main.html", {
        "request": request,
        "sequence": sequence,
        "user_id": id,
        "attendance": userData[f"{id}"]["attendance"]
    })


@app.get("/to_day_study", response_class=HTMLResponse)
async def to_day_study(request: Request):
    user_id = request.session.get('user_id')
    user_data = Load_Json(userDataFile)
    now_stage_idx = user_data[user_id]["now_stage_idx"]
    stage_number = user_data[user_id]["stage"][now_stage_idx]
    print("!")
    print(f"{user_id}")
    print(f"{stage_number}")
    # return templates.TemplateResponse(f"{stage_number}.html", {"request": request})
    return templates.TemplateResponse(f"stage/stage_{stage_number}.html", {"request": request})

@app.post("/clear", response_class=HTMLResponse)
async def submit_form(request: Request, wrong_cnt: int = Form(...), hint_cnt: int = Form(...)):
    
    user_id = request.session.get('user_id')
    user_data = Load_Json(userDataFile)

    # 점수 계산 로직
    point = 50 - (wrong_cnt * 5) - (hint_cnt * 10)
    if point < 0: point = 0
    #

    user_data[user_id]["d_study_count"] += 1
    user_data[user_id]["total_study_count"] += 1
    user_data[user_id]["total_try_count"] += wrong_cnt + 1
    user_data[user_id]["total_wrong_count"] += wrong_cnt
    user_data[user_id]["now_stage_idx"] += 1
    user_data[user_id]["point"] += point

    

    Dump_Json(userDataFile, user_data)
    return templates.TemplateResponse("clear.html", {"request": request, "point": point, "wrong_cnt": wrong_cnt, "hint_cnt": hint_cnt})

# @app.get("/clear_to_main", response_class=HTMLResponse)
# async def clear_to_main(request: Request):
#     return RedirectResponse(url="/main")
# 다음 페이지 
# @app.get("/next", response_class=HTMLResponse)
# async def next(request: Request):
#     user_id = request.session.get('user_id')
#     userData = Load_Json(userDataFile)
#     # now_stage_idx = userData[user_id]["now_stage_idx"] + 1
#     # stage_number = userData[user_id]["stage"][now_stage_idx]
#     # return templates.TemplateResponse(f"{stage_number}.html", {"request": request})
#     return templates.TemplateResponse(f"stage/stage_{stage_number}.html", {"request": request})

@app.get("/collection", response_class=HTMLResponse)
async def shops(request: Request):
    user_id = request.session.get('user_id')
    user_data = Load_Json(userDataFile)

    point = user_data[user_id]["point"]
    return templates.TemplateResponse("collection.html", {"request": request, "user_point": point})
# =======================================