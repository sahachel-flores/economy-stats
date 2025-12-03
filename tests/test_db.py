from app.services.db_tools import *
from app.schemas.news_schema import NewsArticles


def create_test_data():
    test_articles = [{
        "author": "Test Author1",
        "title": "Test Title1",
        "description": "Test Description1",
        "url": "http://test.com",
        "urlToImage": "http://test.com/img.jpg",
        "publishedAt": "2025-01-01",
        "content": "Test content 1"
    },
    {
        "author": "Test Author 2",
        "title": "Test Title 2",
        "description": "Test Description 2",
        "url": "http://test.com/2",
        "urlToImage": "http://test.com/img.jpg/2",
        "publishedAt": "2025-01-02",
        "content": "Test content 2"
    },
    {
        "author": "Test Author 3",
        "title": "Test Title 3",
        "description": "Test Description 3",
        "url": "http://test.com/3",
        "urlToImage": "http://test.com/img.jpg/3",
        "publishedAt": "2025-01-03",
        "content": "Test content 3"
    },
    {
        "author": "Test Author 4",
        "title": "Test Title 4",
        "description": "Test Description 4",
        "url": "http://test.com/4",
        "urlToImage": "http://test.com/img.jpg/4",
        "publishedAt": "2025-01-04",
        "content": "Test content 4"
    },
    {
        "author": "Test Author 5",
        "title": "Test Title 5",
        "description": "Test Description 5",
        "url": "http://test.com/5",
        "urlToImage": "http://test.com/img.jpg/5",
        "publishedAt": "2025-01-05",
        "content": "Test content 5"
    }]
    return test_articles


def test_add_articles_to_db(db_connection):
    """
    Test the add_articles_to_db function.
    """
    # create test data
    test_articles = [{
        "author": "Test Author",
        "title": "Test Title",
        "description": "Test Description",
        "url": "http://test.com",
        "urlToImage": "http://test.com/img.jpg",
        "publishedAt": "2025-01-01",
        "content": "Test content"
    }]

    # add test data to the database
    result = add_articles_to_db(test_articles, db_connection)
    assert result == True
    assert db_connection.query(NewsArticles).count() == 1


def test_get_articles_using_ids_from_db(db_connection):
    """
    Test the get_articles_using_ids_from_db function.
    """ 
    # create test data
    test_articles = create_test_data()
    add_articles_to_db(test_articles, db_connection)
    #assert db_connection.query(NewsArticles).count() == len(test_articles)

    # test the get_articles_using_ids_from_db function
    ids = [1, 2, 3]
    articles = get_articles_using_ids_from_db(ids, db_connection)
    assert len(articles) == len(ids)
    assert articles[0]['id'] == 1
    assert articles[1]['id'] == 2
    assert articles[2]['id'] == 3


def test_remove_all_articles_from_db(db_connection):
    """
    Test the remove_all_articles_from_db function.
    """
    # create test data
    test_articles = create_test_data()
    add_articles_to_db(test_articles, db_connection)
    assert db_connection.query(NewsArticles).count() == len(test_articles)

    # remove all articles from the database
    remove_all_articles_from_db(db_connection)
    assert db_connection.query(NewsArticles).count() == 0


