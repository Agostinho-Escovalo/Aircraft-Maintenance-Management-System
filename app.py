from flask import Flask, redirect, url_for
from config import Config
from models import db
from routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    register_routes(app)

    # Главная страница — перенаправление на список самолётов
    @app.route('/')
    def index():
        return redirect(url_for('aircraft.list_aircraft'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)