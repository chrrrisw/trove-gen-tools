import json
import requests
import webbrowser

from trvartdb import Article

BASE_URL = "https://api.trove.nla.gov.au/v2/result"

KEY = ""
BULK_HARVEST = "true"
ZONE = "&zone=newspaper"
QUERY = "&q={search_term}"
DECADE = "&l-decade={decade}"
YEAR = "&l-year={year}"


def query_trove(payload):
    response = requests.get(BASE_URL, params=payload)
    json_response = json.loads(response.text)
    records = json_response["response"]["zone"][0]["records"]
    return records


def collect_articles(filename, db, year_start, year_end):
    payload = {
        "key": "",
        "bulkHarvest": "true",
        "zone": "newspaper",
        "encoding": "json",
        "q": "",
        "s": "*",
        "n": 20,
        "l-decade": 0,
        "l-year": 0,
    }

    with open(filename, "r") as f:
        for l in f:

            # New query, set q
            payload["q"] = l.strip()

            for year in range(year_start, year_end):

                # New year, set s, decade and year
                payload["s"] = "*"
                decade = year // 10
                payload["l-decade"] = decade
                payload["l-year"] = year

                records = query_trove(payload)

                if "article" in records:
                    articles = records["article"]
                    for a in articles:
                        # print(a["title"]["id"])
                        db.add_article(a)

                # This could be done by recursion, but I worry about depth
                while "nextStart" in records:
                    payload["s"] = records["nextStart"]
                    print("nextStart", records["nextStart"])
                    records = query_trove(payload)
                    if "article" in records:
                        articles = records["article"]
                        for a in articles:
                            db.add_article(a)

    db.commit()


def show_article(article_id):
    webbrowser.open(f"https://trove.nla.gov.au/newspaper/article/{article_id}")


def assess_articles(db, year, article_id):
    """
    Open the database and query all articles not assessed.
    For each Article, open a web page and ask the user (on the command line)
    whether the Article is relevant (yes|no|unknown|quit).
    """
    session = db.session

    if article_id is not None:
        articles = session.query(Article).filter_by(article_id=article_id)
    else:
        articles = session.query(Article).filter_by(assessed=False)
        if year is not None:
            articles = articles.filter(Article.date.like(f"{year}%"))

    for article in articles:
        print(article.article_id)
        show_article(article.article_id)
        relevant = input("Relevant (y/n/q/u)")
        if relevant == "y":
            article.assessed = True
            article.relevant = True
        elif relevant == "n":
            article.assessed = True
            article.relevant = False
        elif relevant == "q":
            break
        else:
            pass

    db.commit()
