import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install('uvicorn')
install('python-multipart')
install('fastapi')
install('jinja2')
install('firebase-admin')
install('itsdangerous')