import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:Agostinho94%40@localhost:5432/aircraft_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False