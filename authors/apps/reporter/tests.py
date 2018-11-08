from django.test import TestCase

from .models import ReportArticle
from django.rest_frameworks import APIClient

# Create your tests here.

class ModelsTestCase(TestCase):
    # This is a test suite checks the definition of reports

    def setUp(self):
        self.article = {
                    "article": {
                        "title": "How to train your dragon",
                        "description": "Ever wonder how?",
                        "body": "You have to believe",
                        "tags": ["reactjs", "angularjs", "dragons"],
                        "published": "true"
                                }
                        }
        self.apiclient = APIClient()
        self.report = ReportArticle
        
    def test_if_model_can_report_an_article(self):
        old_report_count = ReportArticle.objects.count()
        self.report.save()
        new_report_count = ReportArticle.objects.count()
        assertNotEqual(old_report_count, new_report_count)