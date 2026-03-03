from flask import Flask
from config import Config
from database import init_db
from auth import auth
from crud import crud

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(auth)
    app.register_blueprint(crud)

    with app.app_context():
        init_db()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)