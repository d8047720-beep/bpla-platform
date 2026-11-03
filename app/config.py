import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

if os.environ.get("VERCEL") == "1":
    DATABASE = os.path.join("/tmp", "bpla.db")
else:
    DATABASE = os.path.join(BASE_DIR, "data", "bpla.db")
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "5000"))
