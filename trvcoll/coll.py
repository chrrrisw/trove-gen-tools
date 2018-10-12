import json
import requests

BASE_URL = "https://api.trove.nla.gov.au/v2/result"

BULK_HARVEST = "true"
ZONE = "newspaper"
ENCODING = "json"


def query_trove(payload):
    try:
        response = requests.get(BASE_URL, params=payload)
    except requests.exceptions.ProxyError as err:
        print(err)
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


def collect_articles(apikey, db, queries, year_start, year_end, state, title):
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

    if state is not None:
        if state in STATES.keys():
            payload["l-state"] = STATES[state]
        else:
            print("State must be one of", list(STATES.keys()))

    if title is not None:
        payload["l-title"] = title

    for query in db.all_queries():

        # New query, set q
        payload["q"] = query.query

        for year in db.all_years():
            print("Processing", payload["q"], year)

            # New year, set s, decade and year
            payload["s"] = "*"
            decade = year // 10
            payload["l-decade"] = decade
            payload["l-year"] = year

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

        db.commit()

    db.commit()
