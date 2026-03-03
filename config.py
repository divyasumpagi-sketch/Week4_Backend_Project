import os

class Config:
    SECRET_KEY = "week4_secret_key"
    DATABASE = os.path.join(os.path.dirname(__file__), "database.db")