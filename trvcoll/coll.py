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


def collect_articles(apikey, db, queries, year_start, year_end):
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
    }

    # Add all the queries to the database
    if queries is not None:
        with open(queries, "r") as f:
            for l in f:
                db.add_query(l.strip())
        db.commit()

    # add all the years to the database
    if year_start is not None and year_end is not None:
        for year in range(year_start, year_end + 1):
            db.add_year(year)
        db.commit()

    for query in db.all_queries():

        # New query, set q
        payload["q"] = query

        db.add_query(payload["q"])

        for year in db.all_years():
            print("Processing", payload["q"], year)

            db.add_year(year)

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
                # print("nextStart", records["nextStart"])
                records = query_trove(payload)
                if "article" in records:
                    articles = records["article"]
                    for a in articles:
                        db.add_article(a)

        db.commit()

    db.commit()
