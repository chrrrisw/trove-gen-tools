import csv
import logging
import os
from . import Base

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
