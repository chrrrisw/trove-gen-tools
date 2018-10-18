import datetime
import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from . import (
    Article,
    Base,
    Category,
    Highlight,
    NewspaperTitle,
    Person,
    Query,
    Year,
    StateLimit,
    TitleLimit,
)

logger = logging.getLogger(__name__)


CATEGORIES = {
    "Article": 1,
    "Advertising": 2,
    "Detailed lists, results, guides": 3,
    "Family Notices": 4,
    "Literature": 5,
    "Government Gazette Notices": 6,
    "Government Gazette Tenders and Contracts": 7,
    "Government Gazette Proclamations And Legislation": 8,
    "Government Gazette Private Notices": 9,
    "Government Gazette Budgetary Papers": 10,
    "Government Gazette Index And Contents": 11,
    "Government Gazette Appointments And Employment": 12,
    "Government Gazette Freedom Of Information": 13,
}


class ArticleDB(object):
    def __init__(self, dbname):
        self.dbname = dbname
        self._session = None

        if os.path.exists(self.dbname):
            self.bind_db()
        else:
            self.init_db()

    def init_db(self):
        logger.info("Initialising DB")
        self.engine = create_engine(f"sqlite:///{self.dbname}", echo=False)
        Base.metadata.create_all(self.engine)
        DBSession = sessionmaker(bind=self.engine)
        self._session = DBSession()

        for key, value in CATEGORIES.items():
            new_category = Category(id=value, category=key)
            self._session.add(new_category)
        self._session.commit()

    def bind_db(self):
        logger.info("Binding DB")
        self.engine = create_engine(f"sqlite:///{self.dbname}", echo=False)
        Base.metadata.bind = self.engine
        DBSession = sessionmaker(bind=self.engine)
        self._session = DBSession()

    def commit(self):
        logger.info("Committing DB")
        self._session.commit()

    def close(self):
        logger.info("Closing DB")
        self._session.close()

    @property
    def session(self):
        return self._session

    # ARTICLE METHODS

    def add_article(self, article: Article):
        self._session.add(article)

    def add_json_article(self, json_article: dict, query: Query = None):

        # Check for the newspaper title, only add if missing
        existing_title = (
            self._session.query(NewspaperTitle)
            .filter(NewspaperTitle.id == json_article["title"]["id"])
            .one_or_none()
        )
        if existing_title is None:
            logger.debug("%d is new title", json_article["title"]["id"])
            new_title = NewspaperTitle(
                id=json_article["title"]["id"], title=json_article["title"]["value"]
            )
            self._session.add(new_title)

        # Check for the article, only add if missing
        existing_article = (
            self._session.query(Article)
            .filter(Article.id == json_article["id"])
            .one_or_none()
        )
        if existing_article is None:
            logger.debug("%d is new article", json_article["id"])
            new_article = Article(
                id=json_article["id"],
                title_id=json_article["title"]["id"],
                category_id=CATEGORIES[json_article["category"]],
                page=json_article["page"],
                assessed=False,
                relevant=False,
                correctionCount=json_article["correctionCount"],
                illustrated=(json_article["illustrated"].lower() == "y"),
                wordCount=json_article["wordCount"],
                # date=json_article["date"],
                date=datetime.datetime.strptime(
                    json_article["date"], "%Y-%m-%d"
                ).date(),
                heading=json_article.get("heading", ""),
            )
            self._session.add(new_article)
            if query is not None:
                # TODO: Does this only make the link once?
                new_article.queries.append(query)
        else:
            if existing_article.heading != json_article.get("heading", ""):
                logger.debug("HEADING CHANGED")
                logger.debug(
                    "From '%s' to '%s'",
                    existing_article.heading,
                    json_article.get("heading", ""),
                )
                existing_article.heading = json_article.get("heading", "")
            if query is not None:
                # TODO: Does this only make the link once?
                existing_article.queries.append(query)

    def set_assessed(self, article_id, assessed):
        if type(assessed) == str:
            assessed = assessed.lower() == "true"
        logger.debug("Setting assessed to %s", assessed)
        article_query = (
            self._session.query(Article).filter(Article.id == article_id).one_or_none()
        )
        if article_query is not None:
            article_query.assessed = assessed
            self._session.commit()

    def set_relevant(self, article_id, relevant):
        if type(relevant) == str:
            relevant = relevant.lower() == "true"
        logger.debug("Setting relevant to %s", relevant)
        article_query = (
            self._session.query(Article).filter(Article.id == article_id).one_or_none()
        )
        if article_query is not None:
            article_query.relevant = relevant
            self._session.commit()

    # PERSON METHODS

    def add_person(self, name, article=None):
        existing_person = (
            self._session.query(Person).filter(Person.name == name).one_or_none()
        )
        if existing_person is None:
            new_person = Person(name=name, date_of_birth="", date_of_death="")
            self._session.add(new_person)
            if article is not None:
                # TODO: Does this only make the link once?
                article.people.append(new_person)
        else:
            if article is not None:
                # TODO: Does this only make the link once?
                article.people.append(existing_person)

    def all_people(self):
        return self._session.query(Person)

    def set_name(self, person_id, name):
        person_query = (
            self._session.query(Person).filter(Person.id == person_id).one_or_none()
        )
        if person_query is not None:
            person_query.name = name
            self._session.commit()

    def set_dob(self, person_id, dob):
        person_query = (
            self._session.query(Person).filter(Person.id == person_id).one_or_none()
        )
        if person_query is not None:
            person_query.date_of_birth = dob
            self._session.commit()

    def set_dod(self, person_id, dod):
        person_query = (
            self._session.query(Person).filter(Person.id == person_id).one_or_none()
        )
        if person_query is not None:
            person_query.date_of_death = dod
            self._session.commit()

    # QUERY METHODS

    def add_query(self, query: str, article: Article = None):
        """
        Add a query to the database.

        Queries are passed to Trove in the initial collection phase.
        """
        existing_query = (
            self._session.query(Query).filter(Query.query == query).one_or_none()
        )
        if existing_query is None:
            new_query = Query(query=query)
            self._session.add(new_query)
            if article is not None:
                # TODO: Does this only make the link once?
                article.queries.append(new_query)
        else:
            if article is not None:
                # TODO: Does this only make the link once?
                article.queries.append(existing_query)

    def all_query_strings(self):
        """Return a list of the query strings."""
        return [q.query for q in self._session.query(Query)]

    def all_queries(self):
        """Return the queries."""
        return self._session.query(Query)

    # HIGHLIGHT METHODS

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

    # YEAR METHODS

    def add_year(self, year: int) -> None:
        """
        Add a year to the database.

        Years are passed to Trove in the initial collection phase.
        """
        year_query = self._session.query(Year).filter(Year.year == year).one_or_none()
        if year_query is None:
            self._session.add(Year(year=year))

    def all_years(self) -> list:
        return [y.year for y in self._session.query(Year)]

    # STATE LIMIT METHODS

    def add_state_limit(self, state: str) -> None:
        """
        Add a state limit to the database.

        State Limits are passed to Trove in the initial collection phase.
        """
        existing_state = (
            self._session.query(StateLimit)
            .filter(StateLimit.state == state)
            .one_or_none()
        )
        if existing_state is None:
            self._session.add(StateLimit(state=state))

    def all_state_limits(self) -> list:
        """Returns a list of strings, representing the state limits"""

        # return [y.year for y in self._session.query(Year)]
        existing_states = [s.state for s in self._session.query(StateLimit)]
        return existing_states

    # TITLE LIMIT METHODS

    def add_title_limit(self, title: int) -> None:
        """
        Add a title limit to the database.

        Title Limits are passed to Trove in the initial collection phase.
        """
        existing_title = (
            self._session.query(TitleLimit)
            .filter(TitleLimit.title == title)
            .one_or_none()
        )
        if existing_title is None:
            self._session.add(TitleLimit(title=title))

    def all_title_limits(self) -> list:
        """Returns a list of integers, representing the title limits."""

        # return [y.year for y in self._session.query(Year)]
        existing_titles = [t.title for t in self._session.query(TitleLimit)]
        return existing_titles
