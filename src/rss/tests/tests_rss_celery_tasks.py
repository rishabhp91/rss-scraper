from unittest.mock import patch
from django.test import TestCase
import unittest


class RSSCeleryTasksTest(TestCase):
    """
    TestCase class for all celery tasks in RSS app
    """

    @patch("src.rss.tasks.disabled_feed_notification")
    @patch("src.rss.tasks.extract_rss.apply_async")
    @patch("src.rss.models.RSSFeed")
    @patch("feedparser.parse")
    def test_extract_rss(self, mocked_feedparser_parse, mocked_rss_feed, mocked_apply_async, mocked_disabled_feed_notification):
        from src.rss.tasks import extract_rss
        mocked_feedparser_parse.side_effect = Exception("Failed parser for site")
        
        # First attempt to extract
        extract_rss(1, "https://example.sendcloud.com")
        # Second attempt to extract
        extract_rss(1, "https://example.sendcloud.com", 2)
        # Third attempt to extract
        extract_rss(1, "https://example.sendcloud.com", 3)
        # Fourth attempt to extract
        extract_rss(1, "https://example.sendcloud.com", 4)
        # Fifth attempt to extract
        extract_rss(1, "https://example.sendcloud.com", 5)

        # Matching RSS feed with ID=1
        matching_rss_feed = mocked_rss_feed.objects.get.return_value
        self.assertEqual(False, matching_rss_feed.is_active)
        self.assertEqual(1, matching_rss_feed.save.call_count)
        self.assertEqual(1, mocked_disabled_feed_notification.apply_async.call_count)
        

if __name__ == "__main__":
    unittest.main()
