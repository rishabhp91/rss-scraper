# Python modules
from celery import shared_task
from dateutil import parser

# Third party modules
import feedparser


MAX_ATTEMPT_FOR_RSS_EXTRACTION = 5


"""
Asynchronous task to send mail notification
"""
@shared_task()
def disabled_feed_notification(feed_id, feed_url):
    def send_mail(emails, subject=None, body=None):
        # TODO: Need SES/Sendgrid/mailChimp for sending mails
        pass

    from src.rss.models import RSSFeedActivity
    following_users_email = RSSFeedActivity.objects.filter(feed_id=feed_id, is_followed=True).values_list('user__email', flat=True).distinct()
    send_mail(following_users_email, subject=f"RSS Alert - Stopped feed url <{feed_url}>", body=f"Feed URL: {feed_url} <br> Feed ID: {feed_id}")


"""
Asynchronous task to reextract RSS feed
"""
@shared_task()
def extract_rss(feed_id, url, attempt=1):
    from src.rss.models import FeedItem, RSSFeed

    if attempt == MAX_ATTEMPT_FOR_RSS_EXTRACTION:
        # Mark feed as inactive
        __feed = RSSFeed.objects.get(id=feed_id)
        __feed.is_active = False
        __feed.save()

        # Send notification to user
        disabled_feed_notification.apply_async((feed_id, url))
        return

    try:
        data = feedparser.parse(url)
        for article in data["entries"]:
            # Create Feed items for every link in the RSS
            FeedItem.objects.update_or_create(
                feed_id=feed_id, 
                item=article["link"], 
                title=article.get("title"), 
                base=article.get("base"), 
                summary=article.get("summary"), 
                published=article.get("published"), 
                author=article.get("author")
            )
    except:
        # Retry the extraction
        extract_rss.apply_async((feed_id, url, attempt+1))


"""
Asynchronous task to reextract RSS feed one by one automatically
"""
@shared_task()
def refresh_all_rss():
    from src.rss.models import RSSFeed
    # Schedule feeds one by one for extraction
    for _ in RSSFeed.objects.filter(is_active=True):
        extract_rss.apply_async((_.id, _.url))
