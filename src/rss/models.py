# Python module
import uuid
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

#######################################
# Base class for all models in this app
#######################################
class RSSBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        super(RSSBaseModel, self).save(*args, **kwargs)



"""
RSS feeds information
"""
class RSSFeed(RSSBaseModel):
    name = models.CharField(max_length=128)
    url = models.URLField(max_length=512)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "RSS Feed"
        verbose_name_plural = "RSS Feeds"

    def __str__(self):
        return f"{self.name} - {self.url} - {self.is_active}"


"""
RSS feeds activity (user oriented)
"""
class RSSFeedActivity(RSSBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(RSSFeed, on_delete=models.CASCADE)
    is_followed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "RSS Feed Activity"
        verbose_name_plural = "RSS Feed Activities"

    def __str__(self):
        return f"{self.user.username} - {self.feed.name} - {self.is_followed}"


"""
RSS feeds item information
"""
class FeedItem(RSSBaseModel):
    feed = models.ForeignKey(RSSFeed, on_delete=models.CASCADE)
    # Feed fields
    item = models.CharField(max_length=128)
    title = models.CharField(max_length=256, blank=True, null=True)
    base = models.CharField(max_length=512, blank=True, null=True)
    summary = models.CharField(max_length=1024, blank=True, null=True)
    published = models.CharField(max_length=128, blank=True, null=True)
    author = models.CharField(max_length=128, blank=True, null=True)
    # Status tracker
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Feed Item"
        verbose_name_plural = "Feed Items"

    def __str__(self):
        return f"{self.feed.name} - {self.item} - {self.is_active}"


"""
RSS feeds item activity (user oriented)
"""
class FeedItemActivity(RSSBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(FeedItem, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Feed Item Activity"
        verbose_name_plural = "Feed Item Activities"
        unique_together = (('user', 'item'),)

    def __str__(self):
        return f"{self.user.username} - {self.item.item} - {self.is_read}"
