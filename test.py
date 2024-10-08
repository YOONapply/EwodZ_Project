# # from fastapi import FastAPI, Form
# # from fastapi.responses import HTMLResponse
# # from fastapi.routing import APIRouter

# # app = FastAPI()

# # @app.get("/", response_class=HTMLResponse)
# # async def read_form():
# #     return """
# #     <form action="/submit" method="post">
# #         <input type="text" name="value2" value="asd" placeholder="Enter some text" style="display: none">
# #         <input type="submit" value="Submit">
# #     </form>
# #     """

# # @app.post("/submit")
# # async def submit_form(value2: str = Form(...)):
# #     return {"submitted_value": value2}

# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run(app, host="127.0.0.1", port=8000)

# str_num = "123"
# str_num = int(str_num)
# str_num += 1
# str(str_num)
# str_num = str(str_num)
# print(str_num)
# print(type(str_num))

total_try_count = 1
total_wrong_count = 1
user_now_rate = ( total_try_count - float(total_wrong_count) ) / total_try_count * 100.0
print(user_now_rate)