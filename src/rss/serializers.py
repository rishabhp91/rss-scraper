# Third party module
from rest_framework import serializers

# Local module
from src.rss.models import RSSFeed, RSSFeedActivity, FeedItem, FeedItemActivity


class RSSFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = RSSFeed
        fields = [
            "name",
            "url",
            "created_by",
            "is_active",
        ]
        extra_kwargs = {
            "is_active": {"required": False},
        }


class RSSFeedActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = RSSFeedActivity
        fields = [
            "user",
            "feed",
            "is_followed",
        ]
        extra_kwargs = {
            "is_followed": {"required": False},
        }


class FeedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedItem
        fields = [
            "feed",
            "item",
            "title",
            "base",
            "summary",
            "published",
            "author",
            "is_active",
        ]
        extra_kwargs = {
            "is_active": {"required": False},
        }


class FeedItemActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedItemActivity
        fields = [
            "user",
            "item",
            "is_read",
        ]
        extra_kwargs = {
            "is_read": {"required": False},
        }
