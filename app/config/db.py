from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from os import getenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from flask_jwt_extended import JWTManager

load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()

def create_db_if_not_exists():

    dbname = getenv("DB_NAME")
    user = getenv("DB_USER")
    password = getenv("DB_PASSWORD")
    host = getenv("DB_HOST")

    # Connection
    conn = psycopg2.connect(dbname='postgres', user=user, host=host, password=password)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{dbname}'")
    exists = cursor.fetchone()

    if not exists:
        cursor.execute(f'CREATE DATABASE {dbname}')
        print(f"Database {dbname} created successfully!")
    else:
        print(f"Database {dbname} already exists.")

    cursor.close()
    conn.close()

def init_db(app):

    create_db_if_not_exists()

    # DB CONFIG
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv("SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # JWT CONFIG
    app.config['JWT_SECRET_KEY'] = getenv("JWT_SECRET_KEY")
    app.config['JWT_COOKIE_SECURE'] = False
    app.config['JWT_COOKIE_SAMESITE'] = 'Lax'

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        # db.drop_all()
        # print("Datebase dropped")
        db.create_all()
        print("Database created")
