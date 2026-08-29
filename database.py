from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

import os


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

    episodes = relationship("Episode", back_populates="anime")

class Episode(Base):
    __tablename__ = "episodes"
    id = Column(Integer, primary_key=True)
    anime_id = Column(Integer, ForeignKey("anime.id") , nullable=False)
    episode_number = Column(Integer, nullable=False)
    airing_at = Column(Integer, nullable=False) #unix timestamp
    notified = Column(Boolean, default=False)

    anime = relationship("Anime", back_populates="episodes")

class TrackedAnime(Base):
    __tablename__ = "tracked_anime"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    anime_id = Column(Integer, ForeignKey("anime.id"), nullable=False)

    anime = relationship("Anime")


folder = "data"
os.makedirs(folder, exist_ok=True)
engine = create_engine("sqlite:///data/data.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def get_or_create_user(session, discord_id):
    user = session.query(User).filter_by(discord_id=str(discord_id)).first()
    if user is None:
        user = User(discord_id=str(discord_id))
        session.add(user)
        session.commit()
    return user

def get_or_create_anime(session, anilist_id, title, status):
    anime = session.query(Anime).filter_by(anilist_id=anilist_id).first()
    if anime is None:
        anime = Anime(
            anilist_id=anilist_id,
            title=title,
            status=status,
        )
        session.add(anime)
        session.commit()
    return anime

def save_episodes(session, anime, episode_list):
    # clear out old episodes for this anime first (in case of /update refresh)
    session.query(Episode).filter_by(anime_id=anime.id).delete()

    for ep in episode_list:
        episode = Episode(
            anime_id=anime.id,
            episode_number=ep["episode"],
            airing_at=ep["airingAt"],
        )
        session.add(episode)

    session.commit()

def track_anime(session, discord_id, anilist_id, title, status, schedule):
    anime = get_or_create_anime(session, anilist_id, title, status)
    user = get_or_create_user(session, discord_id)
    tracked = session.query(TrackedAnime).filter_by(user_id=user.id,anime_id=anime.id).first()
    if tracked is None:
        save_episodes(session, anime=anime, episode_list=schedule)
        tracked = TrackedAnime(
            anime_id=anime.id,
            user_id=user.id,
        )
        session.add(tracked)
        session.commit()

def get_user_tracked_list(session,discord_id):
    user = session.query(User).filter_by(discord_id=str(discord_id)).first()
    if user is None:
        return []
    tracked = session.query(TrackedAnime).filter_by(user_id=user.id).all()
    return [t.anime for t in tracked]


