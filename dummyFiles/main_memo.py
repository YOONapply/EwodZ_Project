# uvicorn main:app --reload

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
app = FastAPI()

# Jinja2 템플릿을 사용할 디렉토리 설정
# 렌더링할 파일은 templates 디렉토리안에 있어야함.
templates = Jinja2Templates(directory="templates")

# HTML 페이지를 반환하는 엔드포인트

# response_class = HTMLResponse
# - 이 엔드포인트가 반환할 형식이 HTML이라는 걸 FastApip에게 알려줌. -> HTML 반환
#   기본적으로 Json을 반환함.

# async
# - 비동기

# request: Request 파라미터
# - FastAPI의 Request 객체,
#   클라이언트의 요청을 request 변수에 담아서 파라미터로 전달

# "request": request
# - Jinja2에서 사용 가능한 객체
#   위에서 받아온 정보를 클라이언트에게 넘겨줌
@app.get("/signIn", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("signIn.html", {"request": request})



# 폼 데이터를 처리하는 엔드포인트

# name: str = Form(...) 파라미터
# - Form(...) = HTML 폼에서 전송된 데이터를 읽어옴
#   무슨 데이터를 읽어올지는 html 태그의 name 속성에 따라 갈림
@app.post("/submit")
async def submit_form(id: str = Form(...), pw: str = Form(...)):
    print(id)
    return {f"{id}, {pw}"}
