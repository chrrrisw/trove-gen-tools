import os

from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

Base = declarative_base()


class NewspaperTitle(Base):
    """The table to hold Newspaper Titles"""

    __tablename__ = "title"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    articles = relationship("Article")  # One to many, title is parent


article_person = Table(
    "article_person",
    Base.metadata,
    Column("article_id", Integer, ForeignKey("article.id")),
    Column("person_id", Integer, ForeignKey("person.id")),
)


class Person(Base):
    __tablename__ = "person"
    id = Column(Integer, primary_key=True)
    articles = relationship(
        "Article", secondary=article_person, back_populates="people"
    )
    name = Column(String)
    date_of_birth = Column(String)
    date_of_death = Column(String)


class Article(Base):
    __tablename__ = "article"
    id = Column(Integer, primary_key=True)
    title_id = Column(Integer, ForeignKey("title.id"))
    people = relationship(
        "Person", secondary=article_person, back_populates="articles"
    )
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

        # Check for the newspaper title, only add if missing
        title_query = (
            self._session.query(NewspaperTitle)
            .filter(NewspaperTitle.id == json_article["title"]["id"])
            .one_or_none()
        )
        if title_query is None:
            print(json_article["title"]["id"], "is new title")
            title = NewspaperTitle(
                id=json_article["title"]["id"], title=json_article["title"]["value"]
            )
            self._session.add(title)

        # Check for the article, only add if missing
        article_query = (
            self._session.query(Article)
            .filter(Article.id == json_article["id"])
            .one_or_none()
        )
        if article_query is None:
            print(json_article["id"], "is new article")
            article = Article(
                id=json_article["id"],
                title_id=json_article["title"]["id"],
                page=json_article["page"],
                assessed=False,
                relevant=False,
                date=json_article["date"],
                category=json_article["category"],
                heading=json_article.get("heading", ""),
            )
            self._session.add(article)

    def add_person(self, name, article=None):
        name_query = (
            self._session.query(Person).filter(Person.name == name).one_or_none()
        )
        if name_query is None:
            person = Person(name=name)
            self._session.add(person)
            if article is not None:
                article.people.append(person)
        else:
            if article is not None:
                article.people.append(name_query)

    def all_people(self):
        return self._session.query(Person)

    def commit(self):
        self._session.commit()

    @property
    def session(self):
        return self._session
