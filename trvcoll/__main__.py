import argparse

from trvartdb import ArticleDB

from .coll import collect_articles

YEAR_START = 1820
YEAR_END = 1825


def main():
    parser = argparse.ArgumentParser()
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
        "--state",
        dest="state",
        type=str,
        help="limit search to state",
    )
    parser.add_argument(
        "-t",
        "--title",
        dest="title",
        type=str,
        help="limit search to newspaper title",
    )
    parser.add_argument(
        "--start",
        dest="year_start",
        type=int,
        default=YEAR_START,
        help="retrieve articles from",
    )
    parser.add_argument(
        "--end",
        dest="year_end",
        type=int,
        default=YEAR_END,
        help="retrieve articles to",
    )

    args = parser.parse_args()

    adb = ArticleDB(args.database)

    collect_articles(
        apikey=args.apikey,
        db=adb,
        queries=args.queries,
        year_start=args.year_start,
        year_end=args.year_end,
    )


if __name__ == "__main__":
    main()
