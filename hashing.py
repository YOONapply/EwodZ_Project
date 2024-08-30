import hashlib

def hashing(data):
    hashedData = hashlib.sha256()
    hashedData.update(f"{data}".encode("utf-8"))
    return hashedData.hexdigest()

userPw = hashing("asd1234")
inputPw = input("비밀번호 입력")

try:        
    if userPw == hashing(inputPw):
        print("로그인 성공")
    else:
        print("로그인 실패")
except:
    print("로그인 실패")
