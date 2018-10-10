import csv
import logging
import os
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.engine.reflection import Inspector
import pandas as pd

from . import Article, Base, Highlight, NewspaperTitle, Note, Person, Query, Year

logger = logging.getLogger(__name__)

# Mapping of table name to filename
CSV_NAMES = {
    "article": {"csvname": "{}", "reader": None, "writer": None},
    "highlight": {"csvname": "", "reader": None, "writer": None},
    "title": {"csvname": "", "reader": None, "writer": None},
    "note": {"csvname": "", "reader": None, "writer": None},
    "person": {"csvname": "", "reader": None, "writer": None},
    "query": {"csvname": "", "reader": None, "writer": None},
    "year": {"csvname": "", "reader": None, "writer": None},
    "article_person": {"csvname": "", "reader": None, "writer": None},
    "article_note": {"csvname": "", "reader": None, "writer": None},
    "article_query": {"csvname": "", "reader": None, "writer": None},
}


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

    def import_db_from_xlsx(self, xlsxname):
        # Get a list of table names
        # table_names = [Base.metadata.tables.keys()]

        # Construct a dictionary of the current database tables and corresponding
        # classes
        tables_and_classes = {}
        for c in Base._decl_class_registry.values():
            if hasattr(c, "__table__"):
                print(c.__table__, type(c.__table__), c.__table__.name)
                tables_and_classes[c.__table__.name] = c

        if os.path.exists(xlsxname):
            for table_name in tables_and_classes.keys():
                df = pd.read_excel(xlsxname, sheet_name=table_name)
                df.to_sql()
            pass
        else:
            pass


def export_db_as_csv(db_name):
    """
    Open the database file, use an inspector to get table and column names,
    select everything in each table and write it to a corresponding CSV file.

    Because this method uses reflection, this should not need to change
    as the database structure changes.
    """
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


def export_db_as_xlsx(db_name):
    """
    Open the database file, use an inspector to get table names,
    read each table into a pandas dataframe and write them to corresponding
    sheets in an xlsx file.

    Because this method uses reflection, this should not need to change
    as the database structure changes.
    """
    xlsx_name = f"{os.path.splitext(db_name)[0]}.xlsx"
    writer = pd.ExcelWriter(xlsx_name, engine="xlsxwriter", date_format="YYYY-MM-DD")
    engine = create_engine(f"sqlite:///{db_name}", echo=False)
    inspector = Inspector.from_engine(engine)
    for table_name in inspector.get_table_names():
        print("TABLE", table_name)
        df = pd.read_sql_table(table_name, engine)
        df.to_excel(writer, sheet_name=table_name, index=False)
    writer.save()
