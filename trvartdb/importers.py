import logging
import numpy as np
import os
import pandas as pd

from . import (
    Article,
    Base,
    Category,
    Highlight,
    NewspaperTitle,
    Note,
    Person,
    Query,
    Year,
    StateLimit,
    TitleLimit,
)
from .articledb import ArticleDB


logger = logging.getLogger(__name__)


# A mapping from sheet name to column data types
TABLE_TO_DTYPE = {
    "article": {
        "id": np.int,
        "title_id": np.int,
        "category_id": np.int,
        "page": np.int,
        "assessed": np.int,
        "relevant": np.int,
        "illustrated": np.int,
        "correctionCount": np.int,
        "wordCount": np.int,
        "date": np.datetime64,
        "heading": str,
    },
    "highlight": {"id": np.int, "highlight": str},
    "note": {"id": np.int, "note": str},
    "person": {"id": np.int, "name": str, "date_of_birth": str, "date_of_death": str},
    "query": {"id": np.int, "query": str},
    "title": {"id": np.int, "title": str},
    "category": {"id": np.int, "title": str},
    "year": {"id": np.int, "year": np.int},
    "state_limits": None,
    "title_limits": None,
    "article_note": None,
    "article_person": None,
    "article_query": None,
}


def object_from_row_old(klass, row):
    """
    Create an object of the given class from the DataFrame row.

    Discards any columns not part of the klass definition.

    TODO: Do we want to dynamically add columns to the database given
          extra data in the spreadsheet?
    TODO: Could do this as a dict comprehension
    """
    d = {}
    for key in row.keys():
        if hasattr(klass, key):
            d[key] = row[key]
        else:
            logger.warn("Discarding %s", key)
    return klass(**d)


TYPE_MAP = {
    "INTEGER": int,
    "VARCHAR": str,
    "VARCHAR(20)": str,
    "VARCHAR(50)": str,
    "BOOLEAN": bool,
    "DATE": pd.Timestamp.to_pydatetime,
}


def object_from_row_new(klass, row):
    if klass == Person:
        print(row)
    row_keys = [k for k in row.keys()]
    # print(row_keys)
    d = {}
    for column in klass.__table__.columns:
        # print(column.name, column.type)
        # print(type(row_keys), type(column.name), type(column.type))
        # if str(column.type) == "DATE":
        #     print(row[column.name], type(row[column.name]))
        if column.name in row_keys:
            d[column.name] = TYPE_MAP[str(column.type)](row[column.name])
    return klass(**d)


def import_db_from_xlsx(xlsx_name: str = None, db_name: str = None):
    """
    Rather than use df.to_sql() we need a way to migrate and old database schema
    to a new one, hence this routine uses Base.
    """

    # Get a list of table names
    table_names = [Base.metadata.tables.keys()]
    print(table_names)

    if (db_name is None) or (xlsx_name is None):
        import sys

        if (len(sys.argv) != 3) or ("-h" in sys.argv):
            print(f"Usage: {sys.argv[0]} <xlsx_filename> <database_filename>")
            exit(-1)

        xlsx_name = sys.argv[1]
        db_name = sys.argv[2]

    # Construct a dictionary of the current database tables and corresponding
    # classes
    #
    # TODO: This only finds tables and classes derived from Base
    #
    tables_and_classes = {}
    for klass in Base._decl_class_registry.values():
        if hasattr(klass, "__table__"):
            logger.debug(
                klass.__table__, type(klass.__table__), klass.__table__.name, klass
            )
            tables_and_classes[klass.__table__.name] = {"klass": klass}

    if os.path.exists(xlsx_name):
        excel_file = pd.ExcelFile(xlsx_name)
        for table_name in tables_and_classes.keys():
            logger.debug(table_name)
            if table_name in excel_file.sheet_names:
                tables_and_classes[table_name]["df"] = excel_file.parse(
                    sheet_name=table_name, dtype=TABLE_TO_DTYPE[table_name]
                )
            # df.to_sql()

        # We now have a DataFrame and a Class for each Table

        # Create a new database
        if not os.path.exists(db_name):

            adb = ArticleDB(db_name)
            session = adb.session

            logger.debug("## QUERY")
            if ("query" in tables_and_classes) and (
                "df" in tables_and_classes["query"]
            ):
                for index, row in tables_and_classes["query"]["df"].iterrows():
                    if type(row["id"]) != int:
                        logger.error("query identifier is not int")
                    new_query = object_from_row_new(Query, row)
                    session.add(new_query)
            adb.commit()

            logger.debug("## HIGHLIGHT")
            if ("highlight" in tables_and_classes) and (
                "df" in tables_and_classes["highlight"]
            ):
                for index, row in tables_and_classes["highlight"]["df"].iterrows():
                    if type(row["id"]) != int:
                        logger.error("highlight identifier is not int")
                    new_highlight = object_from_row_new(Highlight, row)
                    session.add(new_highlight)
            adb.commit()

            logger.debug("## YEAR")
            if ("year" in tables_and_classes) and ("df" in tables_and_classes["year"]):
                for index, row in tables_and_classes["year"]["df"].iterrows():
                    if type(row["id"]) != int:
                        logger.error("year identifier is not int")
                    # year_dict = dict(row)
                    # print(year_dict, type(year_dict["id"]), type(year_dict["year"]))
                    # year_dict["id"] = int(year_dict["id"])
                    # year_dict["year"] = int(year_dict["year"])
                    # new_year = object_from_row(Year, year_dict)
                    new_year = object_from_row_new(Year, row)
                    session.add(new_year)
            adb.commit()

            logger.debug("## TITLE")
            if ("title" in tables_and_classes) and (
                "df" in tables_and_classes["title"]
            ):
                for index, row in tables_and_classes["title"]["df"].iterrows():
                    if type(row["id"]) != int:
                        logger.error("title identifier is not int")
                    new_title = object_from_row_new(NewspaperTitle, row)
                    session.add(new_title)
            adb.commit()

            # Not needed, new databases have this table by default.
            #
            # logger.debug("## CATEGORY")
            # if ("category" in tables_and_classes) and (
            #     "df" in tables_and_classes["category"]
            # ):
            #     for index, row in tables_and_classes["category"]["df"].iterrows():
            #         if type(row["id"]) != int:
            #             logger.error("category identifier is not int")
            #         new_category = object_from_row_new(Category, row)
            #         session.add(new_category)
            # adb.commit()

            logger.debug("## PERSON")
            if ("person" in tables_and_classes) and (
                "df" in tables_and_classes["person"]
            ):
                for index, row in tables_and_classes["person"]["df"].iterrows():
                    if type(row["id"]) != int:
                        logger.error("person identifier is not int")
                    new_person = object_from_row_new(Person, row)
                    session.add(new_person)
            adb.commit()

            logger.debug("## NOTE")
            if ("note" in tables_and_classes) and ("df" in tables_and_classes["note"]):
                for index, row in tables_and_classes["note"]["df"].iterrows():
                    if type(row["id"]) != int:
                        logger.error("note identifier is not int")
                    new_note = object_from_row_new(Note, row)
                    session.add(new_note)
            adb.commit()

            logger.debug("## ARTICLE")
            if ("article" in tables_and_classes) and (
                "df" in tables_and_classes["article"]
            ):
                for index, row in tables_and_classes["article"]["df"].iterrows():
                    if type(row["id"]) != int:
                        logger.error("article identifier is not int")
                    new_article = object_from_row_new(Article, row)
                    session.add(new_article)
            adb.commit()

            logger.debug("## STATE LIMITS")
            if ("state_limits" in tables_and_classes) and (
                "df" in tables_and_classes["state_limits"]
            ):
                for index, row in tables_and_classes["state_limits"]["df"].iterrows():
                    if type(row["id"]) != int:
                        logger.error("state_limits identifier is not int")
                    new_state_limit = object_from_row_new(StateLimit, row)
                    session.add(new_state_limit)
            adb.commit()

            logger.debug("## TITLE LIMITS")
            if ("title_limits" in tables_and_classes) and (
                "df" in tables_and_classes["title_limits"]
            ):
                for index, row in tables_and_classes["title_limits"]["df"].iterrows():
                    if type(row["id"]) != int:
                        logger.error("title_limits identifier is not int")
                    new_title_limit = object_from_row_new(TitleLimit, row)
                    session.add(new_title_limit)
            adb.commit()

            # ## NOW LINK SOME TABLES

            # if "article_note" in tables_and_classes:
            #     print("## ARTICLE_NOTE")
            #     for index, row in tables_and_classes["article_note"]["df"].iterrows():
            #         existing_article = session.query(Article).filter(Article.id == row["article_id"]).one()
            #         existing_note = session.query(Note).filter(Note.id == row["note_id"]).one()
            #         existing_article.notes.append(existing_note)
            # adb.commit()

            # if "article_person" in tables_and_classes:
            #     print("## ARTICLE_PERSON")
            #     for index, row in tables_and_classes["article_person"]["df"].iterrows():
            #         existing_article = session.query(Article).filter(Article.id == row["article_id"]).one()
            #         print(existing_article.id)
            #         existing_person = session.query(Person).filter(Person.id == row["person_id"]).one()
            #         print(existing_person.id)
            #         existing_article.people.append(existing_person)
            # adb.commit()

            # if "article_query" in tables_and_classes:
            #     print("## ARTICLE_QUERY")
            #     for index, row in tables_and_classes["article_query"]["df"].iterrows():
            #         existing_article = session.query(Article).filter(Article.id == row["article_id"]).one()
            #         print(existing_article.id)
            #         existing_query = session.query(Query).filter(Query.id == row["query_id"]).one()
            #         existing_article.queries.append(existing_query)
            # adb.commit()

            df = pd.read_excel(
                xlsx_name,
                sheet_name="article_note",
                dtype=TABLE_TO_DTYPE["article_note"],
            )
            for index, row in df.iterrows():
                existing_article = (
                    session.query(Article)
                    .filter(Article.id == int(row["article_id"]))
                    .one()
                )
                existing_note = (
                    session.query(Note).filter(Note.id == int(row["note_id"])).one()
                )
                existing_article.notes.append(existing_note)
            adb.commit()

            df = pd.read_excel(
                xlsx_name,
                sheet_name="article_person",
                dtype=TABLE_TO_DTYPE["article_person"],
            )
            for index, row in df.iterrows():
                existing_article = (
                    session.query(Article)
                    .filter(Article.id == int(row["article_id"]))
                    .one()
                )
                existing_person = (
                    session.query(Person)
                    .filter(Person.id == int(row["person_id"]))
                    .one()
                )
                existing_article.people.append(existing_person)
            adb.commit()

            df = pd.read_excel(
                xlsx_name,
                sheet_name="article_query",
                dtype=TABLE_TO_DTYPE["article_query"],
            )
            for index, row in df.iterrows():
                existing_article = (
                    session.query(Article)
                    .filter(Article.id == int(row["article_id"]))
                    .one()
                )
                existing_query = (
                    session.query(Query).filter(Query.id == int(row["query_id"])).one()
                )
                existing_article.queries.append(existing_query)
            adb.commit()

        else:
            logger.error("Database exists")

    else:
        raise FileNotFoundError(xlsx_name)

    # return tables_and_classes


def import_db_from_csv(csv_name, db_name):
    pass
