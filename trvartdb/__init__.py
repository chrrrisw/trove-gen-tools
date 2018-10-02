import os

from sqlalchemy import Column, Integer, String, Boolean  # , ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker  # , relationship
from sqlalchemy import create_engine

Base = declarative_base()


class NewspaperTitle(Base):
    __tablename__ = "titles"
    id = Column(Integer, primary_key=True)
    title_id = Column(Integer)
    title = Column(String)


class Person(Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    date_of_birth = Column(String)
    date_of_death = Column(String)


class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer)
    title_id = Column(Integer)
    page = Column(Integer)
    assessed = Column(Boolean)
    relevant = Column(Boolean)
    date = Column(String(10))
    category = Column(String)
    heading = Column(String)


class ArticleDB(object):
    def __init__(self, dbname):
        self.dbname = dbname
        self._session = None

        if os.path.exists(self.dbname):
            self.bind_db()
        else:
            self.init_db()

    def init_db(self):
        print("Initialising DB")
        engine = create_engine(f"sqlite:///{self.dbname}", echo=False)
        Base.metadata.create_all(engine)
        DBSession = sessionmaker(bind=engine)
        self._session = DBSession()

    def bind_db(self):
        print("Binding DB")
        engine = create_engine(f"sqlite:///{self.dbname}", echo=False)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self._session = DBSession()

    def add_article(self, json_article):
        # Check we don't have it already
        query = (
            self._session.query(Article)
            .filter(Article.article_id == json_article["id"])
            .one_or_none()
        )
        if query is None:
            print(json_article["id"], "is new article")
            article = Article(
                article_id=json_article["id"],
                title_id=json_article["title"]["id"],
                page=json_article["page"],
                assessed=False,
                relevant=False,
                date=json_article["date"],
                category=json_article["category"],
                heading=json_article.get("heading", ""),
            )
            self._session.add(article)

            title_query = (
                self._session.query(NewspaperTitle)
                .filter(NewspaperTitle.title_id == json_article["title"]["id"])
                .one_or_none()
            )

            if title_query is None:
                print(json_article["title"]["id"], "is new title")
                title = NewspaperTitle(
                    title_id=json_article["title"]["id"],
                    title=json_article["title"]["value"],
                )
                self._session.add(title)

    def commit(self):
        self._session.commit()

    @property
    def session(self):
        return self._session
