import logging

from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

logger = logging.getLogger(__name__)


class NewspaperTitle(Base):
    """The table to hold Newspaper Titles"""

    __tablename__ = "title"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    articles = relationship("Article")  # One to many, title is parent


# Two-way association between Article and Person
article_person = Table(
    "article_person",
    Base.metadata,
    Column("article_id", Integer, ForeignKey("article.id")),
    Column("person_id", Integer, ForeignKey("person.id")),
)


# Two-way association between Article and Note
article_note = Table(
    "article_note",
    Base.metadata,
    Column("article_id", Integer, ForeignKey("article.id")),
    Column("note_id", Integer, ForeignKey("note.id")),
)


# Two-way association between Article and Query
article_query = Table(
    "article_query",
    Base.metadata,
    Column("article_id", Integer, ForeignKey("article.id")),
    Column("query_id", Integer, ForeignKey("query.id")),
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
    queries = relationship("Query", secondary=article_query, back_populates="articles")
    notes = relationship("Note", secondary=article_note, back_populates="articles")
    page = Column(Integer)
    assessed = Column(Boolean)
    relevant = Column(Boolean)
    illustrated = Column(Boolean)
    correctionCount = Column(Integer)
    wordCount = Column(Integer)
    # date = Column(String(10))
    date = Column(Date)
    category = Column(String)
    heading = Column(String)


class Year(Base):
    __tablename__ = "year"
    id = Column(Integer, primary_key=True)
    year = Column(Integer, unique=True)


class Query(Base):
    __tablename__ = "query"
    id = Column(Integer, primary_key=True)
    articles = relationship(
        "Article", secondary=article_query, back_populates="queries"
    )
    query = Column(String)


class Highlight(Base):
    __tablename__ = "highlight"
    id = Column(Integer, primary_key=True)
    highlight = Column(String)


class Note(Base):
    __tablename__ = "note"
    id = Column(Integer, primary_key=True)
    articles = relationship("Article", secondary=article_note, back_populates="notes")
    note = Column(String)
