import argparse
import os
import weakref

from aiohttp import web, WSMsgType, WSCloseCode
from jinja2 import Environment, PackageLoader, select_autoescape

from trvartdb import Article, ArticleDB, Query, Highlight, Year


async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    request.app["websockets"].add(ws)
    try:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                if msg.data == "close":
                    await ws.close()
                elif msg.data.startswith("assessed"):
                    _, article_id, assessment = msg.data.split()
                    request.app["database"].set_assessed(article_id, assessment)
                elif msg.data.startswith("relevant"):
                    _, article_id, relevance = msg.data.split()
                    request.app["database"].set_relevant(article_id, relevance)
                else:
                    await ws.send_str(msg.data + "/answer")
            elif msg.type == WSMsgType.ERROR:
                print("ws connection closed with exception %s" % ws.exception())
    finally:
        request.app["websockets"].discard(ws)

    print("websocket connection closed")

    return ws


async def handle_post(request):

    data = await request.post()

    print(data)
    relevance = data["relevant"]
    article_id = int(data["article_id"])
    people = data["people"].split(",")

    reposted = False
    if article_id != request.app["current_article"].id:
        print(type(article_id), type(request.app["current_article"].id))
        print("######### REPOSTED")
        reposted = True

    if not reposted:
        print("POST", request.app["current_article"].id, relevance, people)

        for person in people:
            if person != "":
                request.app["database"].add_person(
                    person, request.app["current_article"]
                )

        if relevance == "Relevant":
            request.app["current_article"].assessed = True
            request.app["current_article"].relevant = True
        elif relevance == "Not Relevant":
            request.app["current_article"].assessed = True
            request.app["current_article"].relevant = False
        elif relevance == "Skip":
            pass
        else:
            raise NotImplementedError(relevance)

        request.app["database"].commit()

        try:
            request.app["current_article"] = request.app["iterator"].__next__()
        except StopIteration as e:
            return web.Response(text="Finished!")

    print("POST now showing", request.app["current_article"].id)
    return web.Response(
        body=request.app["assessment_template"].render(
            article_id=request.app["current_article"].id,
            people=request.app["database"].all_people(),
            highlights=request.app["database"].get_highlight_str(),
        ),
        content_type="text/html",
    )


async def handle_get(request):
    if request.app["current_article"] is None:
        return web.Response(text="Finished!")
    else:
        print("GET Showing", request.url, request.app["current_article"].id)
        return web.Response(
            body=request.app["assessment_template"].render(
                article_id=request.app["current_article"].id,
                people=request.app["database"].all_people(),
                highlights=request.app["database"].get_highlight_str(),
            ),
            content_type="text/html",
        )

    # name = request.match_info.get("name", "Anonymous")
    # text = "Hello, " + name
    # return web.Response(text=text)


async def handle_articles(request):
    all_articles = request.app["database"].session.query(Article)
    return web.Response(
        body=request.app["articles_template"].render(
            db_title=request.app["dbname"], articles=all_articles
        ),
        content_type="text/html",
    )


async def handle_people(request):
    """Show the page that manages the people in the database."""
    all_people = request.app["database"].all_people()
    return web.Response(
        body=request.app["people_template"].render(
            db_title=request.app["dbname"], people=all_people
        ),
        content_type="text/html",
    )


async def handle_queries(request):
    """Show the page that manages the queries in the database."""
    # all_people = request.app["database"].all_people()
    return web.Response(
        body=request.app["queries_template"].render(
            db_title=request.app["dbname"],
            queries=request.app["database"].session.query(Query),
            highlights=request.app["database"].session.query(Highlight),
            years=request.app["database"].session.query(Year)
        ),
        content_type="text/html",
    )


async def on_startup(app):
    print("Startup called")

    # Create and store the database
    app["database"] = ArticleDB(app["dbname"])

    # If we have highlights, add them to the database
    app["database"].set_highlight_str(app["highlights"])

    # Get all unassessed articles
    session = app["database"].session
    articles = session.query(Article).filter_by(assessed=False)

    # Get an iterator for the articles and retrieve the first
    app["iterator"] = articles.__iter__()
    try:
        app["current_article"] = app["iterator"].__next__()
    except StopIteration as e:
        app["current_article"] = None

    # Get and store page templates
    env = Environment(
        loader=PackageLoader("trveval", "templates"),
        autoescape=select_autoescape(["html"]),
    )
    app["assessment_template"] = env.get_template("assessment.html")
    app["articles_template"] = env.get_template("articles.html")
    app["people_template"] = env.get_template("people.html")
    app["queries_template"] = env.get_template("queries.html")


async def on_cleanup(app):
    print("Cleanup called")
    app["database"].commit()


async def on_shutdown(app):
    print("Shutdown called")
    for ws in set(app["websockets"]):
        await ws.close(code=WSCloseCode.GOING_AWAY, message="Server shutdown")


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = "5000"


def main():
    parser = argparse.ArgumentParser(
        prog="trveval",
        description="Evaluate articles for relevance, updating the database as you go.",
    )
    parser.add_argument(dest="database", help="The database to use.")
    parser.add_argument(
        "-l",
        "--highlights",
        dest="highlights",
        help="The file containing highlights.",
    )
    parser.add_argument(
        "-H",
        "--host",
        dest="host",
        help="Hostname of the app " + "[default %s]" % DEFAULT_HOST,
        default=DEFAULT_HOST,
    )
    parser.add_argument(
        "-P",
        "--port",
        dest="port",
        help="Port for the app " + "[default %s]" % DEFAULT_PORT,
        default=DEFAULT_PORT,
    )
    args = parser.parse_args()

    if args.highlights is None:
        highlights = ""
    else:
        if os.path.exists(args.highlights):
            # TODO: parse file and format
            with open(args.highlights, "r") as f:
                highlights = f.read()
        else:
            # TODO: Hopefully a string of plus separated terms
            highlights = args.highlights

    app = web.Application()
    app["websockets"] = weakref.WeakSet()
    app["dbname"] = args.database
    app["highlights"] = highlights

    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    app.on_shutdown.append(on_shutdown)

    # app.add_routes([web.get("/", handle), web.get("/{name}", handle)])

    # Handler for websocket connections
    app.router.add_route("GET", "/ws", websocket_handler)

    # The assessment page
    app.router.add_route("GET", "/", handle_get)
    app.router.add_route("POST", "/", handle_post)

    # The articles page
    app.router.add_route("GET", "/articles.html", handle_articles)

    # The people page
    app.router.add_route("GET", "/people.html", handle_people)

    # The people page
    app.router.add_route("GET", "/queries.html", handle_queries)

    # static files
    static_path = os.path.join(os.path.dirname(__file__), "static")
    app.router.add_static("/static", static_path)

    # run the server
    web.run_app(app, host=args.host, port=args.port)


if __name__ == "__main__":
    print(__file__, __package__)
    main()
