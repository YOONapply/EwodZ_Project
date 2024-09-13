# from fastapi import FastAPI, Request
# from fastapi import FastAPI
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from starlette.requests import Request
# from app.routes import item_routes
# # import item_routes

# app = FastAPI()

# # 템플릿 디렉토리 설정
# templates = Jinja2Templates(directory="app/templates")

# # 라우트 등록
# app.include_router(user_routes.router)

# @app.get("/", response_class=HTMLResponse)
# async def read_root(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# @app.get("/start", response_class=HTMLResponse)
# async def read_map(request: Request):
#     return templates.TemplateResponse("start.html", {"request": request})
    

list = ["윤지원 : 안녕하세요", "지원 :hi "]
for i in list:
    print(i)