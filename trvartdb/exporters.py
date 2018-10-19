import csv
import logging
import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.reflection import Inspector


logger = logging.getLogger(__name__)


def export_db_as_xlsx(db_name: str = None, xlsx_name: str = None):
    """
    Open the database file, use an inspector to get table names,
    read each table into a pandas dataframe and write them to corresponding
    sheets in an xlsx file.

    Because this method uses reflection, this should not need to change
    as the database structure changes.
    """

    # Called as main function means we need to get db_name from the command line
    if (db_name is None) or (xlsx_name is None):
        import argparse

        parser = argparse.ArgumentParser(
            description="Export a Trove newspaper article database as an xlsx file.",
            epilog="This will overwrite an existing xlsx file if it exists.",
        )
        parser.add_argument(
            "db_name", type=str, help="The filename of the article database."
        )
        parser.add_argument(
            "xlsx_name", type=str, help="The filename of the xlsx file to produce."
        )
        args = parser.parse_args()
        db_name = args.db_name
        xlsx_name = args.xlsx_name

    # Connect to the database
    if os.path.exists(db_name):
        engine = create_engine(f"sqlite:///{db_name}", echo=False)
    else:
        raise FileNotFoundError("The specified database does not exist.")

    # Create an Excel writer using pandas
    writer = pd.ExcelWriter(xlsx_name, engine="xlsxwriter", date_format="YYYY-MM-DD")

    # Create an Inspector to inspect the database
    inspector = Inspector.from_engine(engine)
    for table_name in inspector.get_table_names():
        logger.debug("TABLE", table_name)
        df = pd.read_sql_table(table_name, engine)
        df.to_excel(writer, sheet_name=table_name, index=False)

    # Save the Excel file
    writer.save()


def export_db_as_csv(db_name: str = None, csv_base: str = None):
    """
    Open the database file, use an inspector to get table and column names,
    select everything in each table and write it to a corresponding CSV file.

    Because this method uses reflection, this should not need to change
    as the database structure changes.
    """

    # Called as main function means we need to get db_name from the command line
    if (db_name is None) or (csv_base is None):
        import argparse

        parser = argparse.ArgumentParser(
            description="""Export a Trove newspaper article database as a group
            of CSV files.""",
            epilog="""This will overwrite existing CSV files if they exist.
            <csv_base> will be used as the first part of each CSV file produced,
            such that each CSV file will be named <csv_base>_<table_name>.csv.
            This is required because of the limitations of the CSV format,
            which assumes one table per file.""",
        )
        parser.add_argument(
            "db_name", type=str, help="The filename of the article database."
        )
        parser.add_argument(
            "csv_base", type=str, help="The start of each CSV filename."
        )
        args = parser.parse_args()
        db_name = args.db_name
        csv_base = args.csv_base

    # Create a database engine
    if os.path.exists(db_name):
        engine = create_engine(f"sqlite:///{db_name}", echo=False)
    else:
        raise FileNotFoundError("The specified database does not exist.")

    inspector = Inspector.from_engine(engine)
    for table_name in inspector.get_table_names():
        csv_name = f"{csv_base}_{table_name}.csv"
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
