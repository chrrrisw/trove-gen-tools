import os

from sqlalchemy import Column, Integer, String, Boolean  # ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker  # relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Article(Base):
    __tablename__ = "article"
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer)
    assessed = Column(Boolean)
    relevant = Column(Boolean)
    date = Column(String(10))
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
            print(json_article["id"], "is new")
            article = Article(
                article_id=json_article["id"],
                assessed=False,
                relevant=False,
                date=json_article["date"],
                heading=json_article.get("heading", ""),
            )
            self._session.add(article)

    def commit(self):
        self._session.commit()

    @property
    def session(self):
        return self._session
