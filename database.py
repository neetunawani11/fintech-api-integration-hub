import os 
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

load_dotenv()

database_url = URL.create(
    drivername="postgresql+psycopg",
    username=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    host=os.environ["DB_HOST"],
    port=int(os.environ["DB_PORT"]),
    database=os.environ["DB_NAME"],
)

engine = create_engine(
    database_url,
    connect_args={
        "sslmode": "require",
        "connect_timeout": 10
    },
    pool_pre_ping=True
)

class Base(DeclarativeBase):
    pass


def test_connection():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT version();")
        )
        print("Database connection successful!")
        print(result.scalar())

if __name__ == "__main__":
    test_connection()

