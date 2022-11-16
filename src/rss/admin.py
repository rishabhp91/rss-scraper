# Python modules
from django.contrib import admin

# Local modules
from src.rss.models import RSSFeed, RSSFeedActivity, FeedItem, FeedItemActivity

# Manage these objects through Django Admin
admin.site.register(RSSFeed)
admin.site.register(RSSFeedActivity)
admin.site.register(FeedItem)
admin.site.register(FeedItemActivity)
