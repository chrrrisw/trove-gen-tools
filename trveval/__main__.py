import argparse
import os
from aiohttp import web
from jinja2 import Environment, PackageLoader, select_autoescape

from trvartdb import Article, ArticleDB


async def handle_post(request):
    print(request.url)

    data = await request.post()
    relevance = data["relevant"]

    if relevance == "Relevant":
        print("\tRelevant", request.app["current_article"].article_id)
        request.app["current_article"].assessed = True
        request.app["current_article"].relevant = True
    elif relevance == "Not Relevant":
        print("\tNot Relevant", request.app["current_article"].article_id)
        request.app["current_article"].assessed = True
        request.app["current_article"].relevant = False
    elif relevance == "Skip":
        print("\tSkip", request.app["current_article"].article_id)
    else:
        raise NotImplementedError(relevance)

    request.app["database"].commit()

    try:
        request.app["current_article"] = request.app["iterator"].__next__()
    except StopIteration as e:
        return web.Response(text="Finished!")

    print("POST Showing", request.app["current_article"].article_id)
    return web.Response(
        body=request.app["template"].render(
            article_id=request.app["current_article"].article_id,
            search_terms="",
        ),
        content_type="text/html",
    )


async def handle_get(request):
    if request.app["current_article"] is None:
        return web.Response(text="Finished!")
    else:
        print("GET Showing", request.url, request.app["current_article"].article_id)
        return web.Response(
            body=request.app["template"].render(
                article_id=request.app["current_article"].article_id,
                search_terms="",
            ),
            content_type="text/html",
        )

    # name = request.match_info.get("name", "Anonymous")
    # text = "Hello, " + name
    # return web.Response(text=text)


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
    app["template"] = env.get_template("index.html")


async def on_cleanup(app):
    print("Cleanup called")
    app["database"].commit()


async def on_shutdown(app):
    print("Shutdown called")
    # for ws in set(app['websockets']):
    #     await ws.close(code=WSCloseCode.GOING_AWAY,
    #                    message='Server shutdown')


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = "5000"


def main():
    parser = argparse.ArgumentParser(
        prog="trveval",
        description="Evaluate articles for relevance, updating the database as you go.",
    )
    parser.add_argument(dest="database", help="The database to use.")
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

    app = web.Application()
    app["dbname"] = args.database
    # runner = web.AppRunner(app)
    # await runner.setup()

    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    app.on_shutdown.append(on_shutdown)

    # app.add_routes([web.get("/", handle), web.get("/{name}", handle)])
    app.router.add_route("GET", "/", handle_get)
    app.router.add_route("POST", "/", handle_post)
    static_path = os.path.join(os.path.dirname(__file__), "static")
    app.router.add_static("/static", static_path)

    web.run_app(app, host=args.host, port=args.port)


if __name__ == "__main__":
    print(__file__, __package__)
    main()
