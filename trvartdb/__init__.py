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
    people = relationship("Person", secondary=article_person, back_populates="articles")
    page = Column(Integer)
    assessed = Column(Boolean)
    relevant = Column(Boolean)
    date = Column(String(10))
    category = Column(String)
    heading = Column(String)


class Year(Base):
    __tablename__ = "year"
    id = Column(Integer, primary_key=True)
    year = Column(Integer, unique=True)


class Query(Base):
    __tablename__ = "query"
    id = Column(Integer, primary_key=True)
    query = Column(String)


class Highlight(Base):
    __tablename__ = "highlight"
    id = Column(Integer, primary_key=True)
    highlight = Column(String)


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
            # print(json_article["title"]["id"], "is new title")
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
            # print(json_article["id"], "is new article")
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
        else:
            # TODO: Update article heading if changed on Trove
            pass

    def set_assessed(self, article_id, assessed):
        if type(assessed) == str:
            assessed = assessed.lower() == "true"
        print("setting assessed to", assessed)
        article_query = (
            self._session.query(Article).filter(Article.id == article_id).one_or_none()
        )
        if article_query is not None:
            article_query.assessed = assessed
            self._session.commit()

    def set_relevant(self, article_id, relevant):
        if type(relevant) == str:
            relevant = relevant.lower() == "true"
        print("setting relevant to", relevant)
        article_query = (
            self._session.query(Article).filter(Article.id == article_id).one_or_none()
        )
        if article_query is not None:
            article_query.relevant = relevant
            self._session.commit()

    def add_person(self, name, article=None):
        name_query = (
            self._session.query(Person).filter(Person.name == name).one_or_none()
        )
        if name_query is None:
            person = Person(name=name, date_of_birth="", date_of_death="")
            self._session.add(person)
            if article is not None:
                article.people.append(person)
        else:
            if article is not None:
                article.people.append(name_query)

    def all_people(self):
        return self._session.query(Person)

    def commit(self):
        print("Committing DB")
        self._session.commit()

    @property
    def session(self):
        return self._session

    def add_query(self, query):
        """
        Add a query to the database.

        Queries are passed to Trove in the initial collection phase.
        """
        query_query = (
            self._session.query(Query).filter(Query.query == query).one_or_none()
        )
        if query_query is None:
            self._session.add(Query(query=query))

    def all_queries(self):
        return [q.query for q in self._session.query(Query)]

    def add_highlight(self, highlight):
        """
        Add a highlight to the database.

        Highlights are used in the assessment phase, to highlight terms in the
        article text.
        """
        highlight_query = (
            self._session.query(Highlight)
            .filter(Highlight.highlight == highlight)
            .one_or_none()
        )
        if highlight_query is None:
            self._session.add(Highlight(highlight=highlight))

    def set_highlight_str(self, highlight_str):
        for highlight in highlight_str.split("+"):
            if highlight != "":
                self.add_highlight(highlight)

    def get_highlight_str(self):
        highlight_query = self._session.query(Highlight)
        return "+".join([h.highlight for h in highlight_query])

    def add_year(self, year):
        """
        Add a year to the database.

        Years are passed to Trove in the initial collection phase.
        """
        year_query = self._session.query(Year).filter(Year.year == year).one_or_none()
        if year_query is None:
            self._session.add(Year(year=year))

    def all_years(self):
        return [y.year for y in self._session.query(Year)]
