import json
import logging
import requests

from trvartdb.articledb import ArticleDB

BASE_URL = "https://api.trove.nla.gov.au/v2/result"

BULK_HARVEST = "true"
ZONE = "newspaper"
ENCODING = "json"

logger = logging.getLogger(__name__)


def query_trove(payload):
    try:
        response = requests.get(BASE_URL, params=payload)
    except requests.exceptions.ProxyError as err:
        logger.exception("Error connecting to Trove.")
        return {}
    else:
        json_response = json.loads(response.text)
        records = json_response["response"]["zone"][0]["records"]
        return records


# Get the list of newspaper titles in Trove from a particular state
# https://api.trove.nla.gov.au/v2/newspaper/titles?key=<INSERT KEY>&state=vic
STATES = {
    "int": "International",
    "nsw": "New South Wales",
    "act": "ACT",
    "qld": "Queensland",
    "tas": "Tasmania",
    "sa": "South Australia",
    "nt": "Northern Territory",
    "wa": "Western Australia",
    "vic": "Victoria",
    "national": "National",
}


def collect_articles(
    apikey: str,
    db: ArticleDB,
    queries: str,
    year_start: int,
    year_end: int,
    states: list,
    titles: list,
):
    payload = {
        "key": apikey,
        "bulkHarvest": BULK_HARVEST,
        "zone": ZONE,
        "encoding": ENCODING,
        "q": "",
        "s": "*",
        "n": 20,
        "l-decade": 0,
        "l-year": 0,
        "reclevel": "full",
    }

    # Add all the new queries to the database
    if queries is not None:
        with open(queries, "r") as query_file:
            for line in query_file:
                query = line.strip()
                if query != "":
                    db.add_query(query)
        db.commit()

    # add all the new years to the database
    if year_start is not None and year_end is not None:
        for year in range(year_start, year_end + 1):
            db.add_year(year)
        db.commit()

    if states is not None:
        for state in states:
            if state in STATES.keys():
                db.add_state_limit(STATES[state])
                # payload["l-state"] = STATES[state]
            else:
                print("State must be one of", list(STATES.keys()))
        db.commit()

    if titles is not None:
        for title in titles:
            db.add_title_limit(title)
        db.commit()

    def _do_query():
        print(
            "Processing",
            payload["q"],
            payload["l-year"],
            payload.get("l-state"),
            payload.get("l-title"),
        )

        # Set start
        payload["s"] = "*"

        records = query_trove(payload)

        if "article" in records:
            articles = records["article"]
            for article in articles:
                # print(a["title"]["id"])
                db.add_json_article(json_article=article, query=query)

        # This could be done by recursion, but I worry about depth
        while "nextStart" in records:
            payload["s"] = records["nextStart"]
            # print("nextStart", records["nextStart"])
            records = query_trove(payload)
            if "article" in records:
                articles = records["article"]
                for article in articles:
                    db.add_json_article(json_article=article, query=query)

    for query in db.all_queries():

        # New query, set q
        payload["q"] = query.query

        for year in db.all_years():

            # New year, set decade and year
            decade = year // 10
            payload["l-decade"] = decade
            payload["l-year"] = year

            all_states = db.all_state_limits()
            all_titles = db.all_title_limits()

            if all_states == []:

                if all_titles == []:
                    _do_query()
                else:
                    for title in all_titles:
                        payload["l-title"] = title
                        _do_query()

            else:
                for state in all_states:
                    payload["l-state"] = state

                    if all_titles == []:
                        _do_query()
                    else:
                        for title in all_titles:
                            payload["l-title"] = title
                            _do_query()

                db.commit()

        db.commit()

    db.commit()
