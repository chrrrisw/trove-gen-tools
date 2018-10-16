import csv
import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.engine.reflection import Inspector
import pandas as pd
import numpy as np

from . import Article, Base, Highlight, NewspaperTitle, Note, Person, Query, Year
from .articledb import ArticleDB

logger = logging.getLogger(__name__)


class ArticleCSV(object):
    """A class to handle multiple CSV files as one"""

    def __init__(self):
        # A file to list all the others?
        self.sheet_set = None

        # Each of the files required to import/export the entire database
        self.article = None
        self.highlight = None
        self.title = None
        self.note = None
        self.person = None
        self.query = None
        self.year = None
        self.article_person = None
        self.article_note = None
        self.article_query = None

    def export_db2(self, articledb):
        # for table_name in CSV_NAMES.keys():
        #     print(table_name)
        #     for col in old_article.__table__.columns

        for t in Base.metadata.tables:
            found_classes = set(
                c
                for c in Base._decl_class_registry.values()
                if hasattr(c, "__table__") and c.__table__ is t
            )
            csvname = f"{os.path.splitext(articledb.dbname)[0]}_{t}.csv"
            # print("table:", t, ", csvname:", f"{prefix}_{t}.csv")
            # print(Base.metadata.tables[t].columns)
            # for column in Base.metadata.tables[t].columns:
            #     print(column.name)
            fieldnames = [col.name for col in Base.metadata.tables[t].columns]
            print(csvname, fieldnames, found_classes)
            with open(csvname, "w") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

    def import_db_from_csv(self, csvname):
        if os.path.exists(csvname):
            pass
        else:
            pass


# A mapping from sheet name to column data types
TABLE_TO_DTYPE = {
    "article": {
        "id": np.int,
        "title_id": np.int,
        "page": np.int,
        "assessed": np.int,
        "relevant": np.int,
        "illustrated": np.int,
        "correctionCount": np.int,
        "wordCount": np.int,
        "date": np.datetime64,
        "category": str,
        "heading": str,
    },
    "highlight": {"id": np.int, "highlight": str},
    "note": {"id": np.int, "note": str},
    "person": {"id": np.int, "name": str, "date_of_birth": str, "date_of_death": str},
    "query": {"id": np.int, "query": str},
    "title": {"id": np.int, "title": str},
    "year": {"id": np.int, "year": np.int},
    "article_note": None,
    "article_person": None,
    "article_query": None,
}


def object_from_row(klass, row):
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
    "BOOLEAN": bool,
    "DATE": pd.Timestamp.to_pydatetime,
}


def object_from_row_2(klass, row):
    row_keys = [k for k in row.keys()]
    # print(row_keys)
    d = {}
    for column in klass.__table__.columns:
        # print(column.name, column.type)
        # print(type(row_keys), type(column.name), type(column.type))
        if str(column.type) == "DATE":
            print(row[column.name], type(row[column.name]))
        if column.name in row_keys:
            d[column.name] = TYPE_MAP[str(column.type)](row[column.name])
    return klass(**d)


def import_db_from_xlsx(xlsxname, dbname):
    """
    Rather than use df.to_sql() we need a way to migrate and old database schema
    to a new one, hence this routine uses Base.
    """

    # Get a list of table names
    table_names = [Base.metadata.tables.keys()]
    print(table_names)

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

    if os.path.exists(xlsxname):
        for table_name in tables_and_classes.keys():
            logger.debug(table_name)
            tables_and_classes[table_name]["df"] = pd.read_excel(
                xlsxname, sheet_name=table_name, dtype=TABLE_TO_DTYPE[table_name]
            )
            # df.to_sql()

        # We now have a DataFrame and a Class for each Table

        # Create a new database
        if not os.path.exists(dbname):

            adb = ArticleDB(dbname)
            session = adb.session

            logger.debug("## QUERY")
            if "query" in tables_and_classes:
                for index, row in tables_and_classes["query"]["df"].iterrows():
                    if type(row["id"]) != int:
                        logger.error("query identifier is not int")
                    new_query = object_from_row_2(Query, row)
                    session.add(new_query)
            adb.commit()

            logger.debug("## HIGHLIGHT")
            if "highlight" in tables_and_classes:
                for index, row in tables_and_classes["highlight"]["df"].iterrows():
                    if type(row["id"]) != int:
                        logger.error("highlight identifier is not int")
                    new_highlight = object_from_row_2(Highlight, row)
                    session.add(new_highlight)
            adb.commit()

            logger.debug("## YEAR")
            if "year" in tables_and_classes:
                for index, row in tables_and_classes["year"]["df"].iterrows():
                    if type(row["id"]) != int:
                        logger.error("year identifier is not int")
                    # year_dict = dict(row)
                    # print(year_dict, type(year_dict["id"]), type(year_dict["year"]))
                    # year_dict["id"] = int(year_dict["id"])
                    # year_dict["year"] = int(year_dict["year"])
                    # new_year = object_from_row(Year, year_dict)
                    new_year = object_from_row_2(Year, row)
                    session.add(new_year)
            adb.commit()

            logger.debug("## TITLE")
            if "title" in tables_and_classes:
                for index, row in tables_and_classes["title"]["df"].iterrows():
                    if type(row["id"]) != int:
                        logger.error("title identifier is not int")
                    new_title = object_from_row_2(NewspaperTitle, row)
                    session.add(new_title)
            adb.commit()

            logger.debug("## PERSON")
            if "person" in tables_and_classes:
                for index, row in tables_and_classes["person"]["df"].iterrows():
                    if type(row["id"]) != int:
                        logger.error("person identifier is not int")
                    new_person = object_from_row_2(Person, row)
                    session.add(new_person)
            adb.commit()

            logger.debug("## NOTE")
            if "note" in tables_and_classes:
                for index, row in tables_and_classes["note"]["df"].iterrows():
                    if type(row["id"]) != int:
                        logger.error("note identifier is not int")
                    new_note = object_from_row_2(Note, row)
                    session.add(new_note)
            adb.commit()

            logger.debug("## ARTICLE")
            if "article" in tables_and_classes:
                for index, row in tables_and_classes["article"]["df"].iterrows():
                    if type(row["id"]) != int:
                        logger.error("article identifier is not int")
                    new_article = object_from_row_2(Article, row)
                    session.add(new_article)
            adb.commit()

            ### NOW LINK SOME TABLES

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
                xlsxname,
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
                xlsxname,
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
                xlsxname,
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
        raise FileNotFoundError(xlsxname)

    return tables_and_classes


def export_db_as_csv(db_name: str = None):
    """
    Open the database file, use an inspector to get table and column names,
    select everything in each table and write it to a corresponding CSV file.

    Because this method uses reflection, this should not need to change
    as the database structure changes.
    """

    # Called as main function means we need to get db_name from the command line
    if db_name is None:
        import sys

        if len(sys.argv) < 2:
            print(f"Usage: {sys.argv[0]} <database_filename>")
            exit(-1)
        db_name = sys.argv[1]

    engine = create_engine(f"sqlite:///{db_name}", echo=False)
    inspector = Inspector.from_engine(engine)
    for table_name in inspector.get_table_names():
        csv_name = f"{os.path.splitext(db_name)[0]}_{table_name}.csv"
        columns = [col["name"] for col in inspector.get_columns(table_name)]
        with engine.begin() as conn:
            results = conn.execute(f"select * from {table_name}")
            with open(csv_name, "w", newline="") as csv_file:

                # TODO: RowProxy.keys() is a list, can't use DictWriter
                # writer = csv.DictWriter(csv_file, fieldnames=columns)
                # writer.writeheader()

                writer = csv.writer(csv_file)
                writer.writerow(columns)
                for result in results:
                    writer.writerow(result.values())


def export_db_as_xlsx(db_name: str = None):
    """
    Open the database file, use an inspector to get table names,
    read each table into a pandas dataframe and write them to corresponding
    sheets in an xlsx file.

    Because this method uses reflection, this should not need to change
    as the database structure changes.
    """

    # Called as main function means we need to get db_name from the command line
    if db_name is None:
        import sys

        if len(sys.argv) < 2:
            print(f"Usage: {sys.argv[0]} <database_filename>")
            exit(-1)
        db_name = sys.argv[1]

    xlsx_name = f"{os.path.splitext(db_name)[0]}.xlsx"
    writer = pd.ExcelWriter(xlsx_name, engine="xlsxwriter", date_format="YYYY-MM-DD")
    engine = create_engine(f"sqlite:///{db_name}", echo=False)
    inspector = Inspector.from_engine(engine)
    for table_name in inspector.get_table_names():
        print("TABLE", table_name)
        df = pd.read_sql_table(table_name, engine)
        df.to_excel(writer, sheet_name=table_name, index=False)
    writer.save()
