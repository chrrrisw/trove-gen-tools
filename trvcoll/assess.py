import webbrowser

from trvartdb import Article


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
        articles = session.query(Article).filter_by(id=article_id)
    else:
        articles = session.query(Article).filter_by(assessed=False)
        if year is not None:
            articles = articles.filter(Article.date.like(f"{year}%"))

    for article in articles:
        print(article.id)
        show_article(article.id)
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
