import argparse
from functools import partial
import os
import weakref

from aiohttp import web, WSMsgType, WSCloseCode
from jinja2 import Environment, PackageLoader, select_autoescape

from trvartdb import Article, ArticleDB, Person


async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    request.app["websockets"].add(ws)
    try:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                if msg.data == "close":
                    await ws.close()
                else:
                    await ws.send_str(msg.data + "/answer")
            elif msg.type == WSMsgType.ERROR:
                print("ws connection closed with exception %s" % ws.exception())
    finally:
        request.app["websockets"].discard(ws)

    print("websocket connection closed")

    return ws


async def handle_post(search_terms, request):

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
                request.app["database"].add_person(person, request.app["current_article"])

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
        body=request.app["index_template"].render(
            article_id=request.app["current_article"].id,
            people=request.app["database"].all_people(),
            search_terms=search_terms,
        ),
        content_type="text/html",
    )


async def handle_get(search_terms, request):
    if request.app["current_article"] is None:
        return web.Response(text="Finished!")
    else:
        print("GET Showing", request.url, request.app["current_article"].id)
        return web.Response(
            body=request.app["index_template"].render(
                article_id=request.app["current_article"].id,
                people=request.app["database"].all_people(),
                search_terms=search_terms,
            ),
            content_type="text/html",
        )

    # name = request.match_info.get("name", "Anonymous")
    # text = "Hello, " + name
    # return web.Response(text=text)


async def handle_db(request):
    all_articles = request.app["database"].session.query(Article)
    return web.Response(
        body=request.app["db_template"].render(
            db_title=request.app["dbname"], articles=all_articles
        ),
        content_type="text/html",
    )


async def on_startup(app):
    print("Startup called")
    app["database"] = ArticleDB(app["dbname"])
    session = app["database"].session
    articles = session.query(Article).filter_by(assessed=False)
    app["iterator"] = articles.__iter__()
    try:
        app["current_article"] = app["iterator"].__next__()
    except StopIteration as e:
        app["current_article"] = None

    env = Environment(
        loader=PackageLoader("trveval", "templates"),
        autoescape=select_autoescape(["html"]),
    )
    app["index_template"] = env.get_template("index.html")
    app["db_template"] = env.get_template("db.html")


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
        "-s",
        "--search_terms",
        dest="search_terms",
        help="The file containing search terms.",
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

    if args.search_terms is None:
        print("No search terms")
        search_terms = ""
    else:
        if os.path.exists(args.search_terms):
            # TODO: parse file and format
            with open(args.search_terms, "r") as f:
                search_terms = f.read()
        else:
            # TODO: Hopefully a string of plus separated terms
            search_terms = args.search_terms

    getcb = partial(handle_get, search_terms)
    postcb = partial(handle_post, search_terms)

    app = web.Application()
    app["websockets"] = weakref.WeakSet()
    app["dbname"] = args.database
    # runner = web.AppRunner(app)
    # await runner.setup()

    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    app.on_shutdown.append(on_shutdown)

    # app.add_routes([web.get("/", handle), web.get("/{name}", handle)])
    app.router.add_route("GET", "/ws", websocket_handler)
    app.router.add_route("GET", "/", getcb)
    app.router.add_route("GET", "/db.html", handle_db)
    app.router.add_route("POST", "/", postcb)
    static_path = os.path.join(os.path.dirname(__file__), "static")
    app.router.add_static("/static", static_path)

    web.run_app(app, host=args.host, port=args.port)


if __name__ == "__main__":
    print(__file__, __package__)
    main()
