from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base



Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    discord_id = Column(String, unique=True, nullable=False)

class Anime(Base):
    __tablename__ = "anime"
    id = Column(Integer, primary_key=True)
    anilist_id = Column(Integer, unique=True, nullable=False)
    title = Column(String, nullable=False)
    status = Column(String)

class Episode(Base):
    __tablename__ = "episodes"
    id = Column(Integer, primary_key=True)
    anime_id = Column(Integer, ForeignKey("anime.id") , nullable=False)
    episode_number = Column(Integer, nullable=False)
    airing_at = Column(Integer, nullable=False) #unix timestamp
    notified = Column(Boolean, default=False)

class TrackedAnime(Base):
    __tablename__ = "tracked_anime"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    anime_id = Column(Integer, ForeignKey("anime.id"), nullable=False)


engine = create_engine("sqlite:///data/data.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
