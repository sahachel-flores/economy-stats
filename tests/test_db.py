from app.services.db_tools import *
from app.services.news_api_tools import get_news_articles_from_news_api
from app.models.agent_context_schema import AgentContext
from tests.init_db_session import SessionLocal
# create test db
def create_test_data():
    """
    Create test data for the database.
    """
    db = SessionLocal()
    context = AgentContext()
    articles = get_news_articles_from_news_api(query="US Economy", from_date="2025-09-16", to_date="2025-09-17", context=context, db=db)
    return articles


def test_add_article_to_db():
    """
    Test the add_article_to_db function.
    """
    db = SessionLocal()
    articles = create_test_data()
    add_articles_to_db(articles)
    assert len(articles) == len(db.query(NewsArticles).all())
    db.close()


def test_get_all_articles_from_db():
    """
    Test the get_all_articles_from_db function.
    """
    db = SessionLocal()
    assert len(db.query(NewsArticles).all()) > 0
    db.close()

def test_get_articles_using_ids_from_db():
    """
    Test the get_articles_using_ids_from_db function.
    """
    ids = [1, 2, 3]
    db = SessionLocal()
    articles = get_articles_using_ids_from_db(ids, db)
    assert len(articles) == len(ids) 
    db.close()



def test_test_db_has_items():
    """
    Test the test_db_has_items function.
    """
    db = SessionLocal()
    assert test_db_has_items(db)
    db.close()

def test_remove_all_articles_from_db():
    """
    Test the remove_all_articles_from_db function.
    """
    db = SessionLocal()
    remove_all_articles_from_db(db)
    assert len(get_all_articles_from_db(db)) == 0
    db.close()

if __name__ == "__main__":
    test_add_article_to_db()
    test_get_all_articles_from_db()
    test_get_articles_using_ids_from_db()
    test_test_db_has_items()
    test_remove_all_articles_from_db()