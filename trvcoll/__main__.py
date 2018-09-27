import argparse

from trvartdb import ArticleDB

from .coll import assess_articles, collect_articles

YEAR_START = 1820
YEAR_END = 1866


parser = argparse.ArgumentParser()
parser.add_argument(
    dest="filename",
    help="The file that contains the search strings (one per line).",
)
parser.add_argument(
    dest="database", help="The database in which to store the results."
)
parser.add_argument(
    "-a",
    "--assess",
    action="store_true",
    dest="assess",
    help="assess articles in browser",
)
parser.add_argument(
    "-y", "--year", dest="year", help="limit assessment to this year"
)
parser.add_argument(
    "-n", "--article", dest="article", help="limit assessment to this article"
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

if args.assess:
    assess_articles(db=adb, year=args.year, article_id=args.article)
else:
    collect_articles(
        filename=args.filename,
        db=adb,
        year_start=args.year_start,
        year_end=args.year_end,
    )
