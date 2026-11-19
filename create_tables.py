

from database import Base, engine
from models import User, Account

print("Creating missing database tables...")

Base.metadata.create_all(bind=engine)

print("Database table setup completed!")

