from . import BaseAPITestCase


class TestArticleFilters(BaseAPITestCase):

    def setUp(self):
        super().setUp()
        self.authenticate()

    def test_it_filters_articles_by_article_title(self):

        self.create_article()
        self.create_article(title="Some article with another title")
        response = self.client.get(
            "/api/articles/?title=Some article with another title"
        )
        self.assertEqual(len(response.data['results']), 1)

    def test_it_filters_articles_by_article_tag(self):
        self.create_article()
        self.create_article(tagList=['learning', 'django'])
        self.create_article(tagList=['learning', 'vuejs', "aws", "jest"])
        response = self.client.get("/api/articles/?tag=learning")
        self.assertEqual(len(response.data['results']), 2)

    def test_it_filters_articles_by_article_description(self):
        description = "Testing django apps"
        self.create_article(description=description)
        response = self.client.get(
            f"/api/articles/?description={description}"
        )
        self.assertEqual(len(response.data['results']), 1)

    def test_it_filters_articles_by_author_username(self):
        self.create_articles_with_diferent_authors()
        response = self.client.get("/api/articles/?author=krm")
        self.assertEqual(len(response.data['results']), 1)

    def test_it_filters_articles_by_author_email(self):
        self.create_articles_with_diferent_authors()
        response = self.client.get("/api/articles/?author=krm@example.com")
        self.assertEqual(len(response.data['results']), 1)

    def create_articles_with_diferent_authors(self):
        self.create_article()
        self.authenticate(
            {"username": "krm", "email": "krm@example.com"}
        )
        self.create_article()

    def create_article(self, **kwargs):
        article = {
            "title": "How to train your dragon",
            "description": "Ever wonder how?",
            "body": "You have to believe",
            "tagList": ["reactjs", "angularjs", "dragons"],
            "published": True
        }
        data = {**article}
        data.update(kwargs)
        self.client.post("/api/articles/", {"article": data})
