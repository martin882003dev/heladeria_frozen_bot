from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from bot.config import settings

engine = create_engine(settings.db.url)
Session = sessionmaker(bind=engine)
Base = declarative_base()