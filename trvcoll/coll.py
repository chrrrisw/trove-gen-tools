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


def collect_articles(apikey, filename, db, year_start, year_end):
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

    with open(filename, "r") as f:
        for l in f:

            # New query, set q
            payload["q"] = l.strip()

            db.add_query(payload["q"])

            for year in range(year_start, year_end + 1):
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
