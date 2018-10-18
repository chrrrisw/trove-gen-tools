import argparse
import logging

from trvartdb.articledb import ArticleDB

from .coll import collect_articles

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="A utility to search Trove for given queries within given bounds.",
        epilog="""States should be a comma-separated list of state abbreviations.
        Titles should be a comma-separated list of newspaper title identifiers.""",
    )
    parser.add_argument(dest="apikey", help="Your Trove API key.")
    parser.add_argument(
        dest="database", help="The database in which to store the results."
    )
    parser.add_argument(
        "-q",
        "--queries",
        dest="queries",
        help="A file that contains queries (one per line).",
    )
    parser.add_argument(
        "-s",
        "--states",
        dest="states",
        type=str,
        help="limit search to state(s) - comma separated",
    )
    parser.add_argument(
        "-t",
        "--titles",
        dest="titles",
        type=str,
        help="limit search to newspaper title(s) - comma separated",
    )
    parser.add_argument(
        "--start", dest="year_start", type=int, help="retrieve articles from year"
    )
    parser.add_argument(
        "--end", dest="year_end", type=int, help="retrieve articles to year"
    )

    args = parser.parse_args()

    adb = ArticleDB(args.database)

    if len(adb.all_query_strings()) == 0 and args.queries is None:
        print("You must specify some queries (-q) for a new database")
        exit(-1)

    if len(adb.all_years()) == 0 and (
        (args.year_start is None) or (args.year_end is None)
    ):
        print("You must specify a year range for a new database")
        exit(-1)

    if args.states is not None:
        states = args.states.split(",")
    else:
        states = None

    if args.titles is not None:
        titles = args.titles.split(",")
    else:
        titles = None

    collect_articles(
        apikey=args.apikey,
        db=adb,
        queries=args.queries,
        year_start=args.year_start,
        year_end=args.year_end,
        states=states,
        titles=titles,
    )


if __name__ == "__main__":
    main()
