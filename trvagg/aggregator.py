from trvartdb import ArticleDB, Article

# TODO: Cannot rely on IDs being same between databases - search on name, etc


class Aggregator(object):
    """Reads one ArticleDB and transfers relevant articles to another."""

    def __init__(self, from_dbname, to_dbname):
        super(Aggregator, self).__init__()
        self.from_db = ArticleDB(from_dbname)
        self.to_db = ArticleDB(to_dbname)

        # TODO: Copy titles, people, etc

        from_articles = self.from_db.session.query(Article).filter_by(relevant=True)
        for old_article in from_articles:
            new_article = Article()
            [
                setattr(new_article, col.name, getattr(old_article, col.name))
                for col in old_article.__table__.columns
            ]
            self.to_db.add_article(new_article)

        self.to_db.commit()

    def new_object(self, from_object):
        new_instance = from_object.__class__()
        [
            setattr(new_instance, col.name, getattr(from_object, col.name))
            for col in from_object.__table__.columns
        ]
        return new_instance

    def copy_titles(self):
        pass

    def copy_articles(self):
        pass

    def copy_people(self):
        pass

    def copy_queries(self):
        pass
