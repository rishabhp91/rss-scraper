# Python modules
import json
import logging
import re
from django.forms.models import model_to_dict
from dateutil import parser

# Third party modules
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Local modules
from src.rss.serializers import RSSFeedSerializer, RSSFeedActivitySerializer, FeedItemSerializer, FeedItemActivitySerializer
from src.rss.models import RSSFeed, RSSFeedActivity, FeedItem, FeedItemActivity

logger = logging.getLogger(__name__)


class RSSFeedsView(APIView):
    """
    View to returns a list of RSS feeds and createw new RSS feed
        Supported methods: GET, POST
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        requested_owned = request.GET.get("owned", False)

        rss_feeds = []
        if requested_owned:
            # List all owned feeds
            user = request.user
            rss_feeds = RSSFeed.objects.filter(created_by=user)
            logger.info(f"Fetching owned RSS for user<{user.id}>")
        else:
            # List all feeds
            rss_feeds = RSSFeed.objects.all()
            logger.info(f"Fetching all RSS")

        feeds = []
        for feed in rss_feeds:
            tmp_dict = model_to_dict(feed)
            feeds.append(tmp_dict)

        return Response(feeds, 200)

    def post(self, request):
        params = {}
        status = 200
        data = json.loads(request.body)
        data["created_by"] = request.user.id
        feed = RSSFeedSerializer(data=data)
        if feed.is_valid() is True:
            feed_obj = feed.save()
            # Submit job to scrape/extract the RSS
            from src.rss.tasks import extract_rss
            task_id = extract_rss.apply_async((feed_obj.id, feed_obj.url))
            params["rss-scraper-job"] = str(task_id)
        else:
            status = 400
            params["errors"] = feed.errors
        return Response(params, status)


class RSSFeedView(APIView):
    """
    View to perform URD on RSS feed
        Supported methods: GET, DELETE, PUT
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, feed_id):
        feed_obj = None
        try:
            feed_obj = RSSFeed.objects.get(id=feed_id)
        except RSSFeed.DoesNotExist:
            params = {}
            params["message"] = f"RSS Feed with id {feed_id} does not exist"
            return Response(params, 404)
        
        feed_items = FeedItem.objects.filter(feed=feed_obj)
        __items = []
        if feed_items.exists():
            for item in feed_items:
                tmp_dict = model_to_dict(item)
                __items.append(tmp_dict)

        feed_dict = model_to_dict(feed_obj)
        feed_dict["items"] = __items
        return Response(feed_dict, 200)

    def delete(self, request, feed_id):
        params = {}
        status = 200
        user = request.user
        try:
            feed_obj = RSSFeed.objects.get(id=feed_id, created_by=user)
        except RSSFeed.DoesNotExist:
            params["message"] = f"RSS Feed with id {feed_id} does not exist"
            status = 404
            return Response(params, status)

        feed_obj.delete()
        params["message"] = "Feed was successfully deleted"

        return Response(params, status)

    def put(self, request, feed_id):
        feed_obj = None
        user = request.user
        try:
            feed_obj = RSSFeed.objects.get(id=feed_id, created_by=user)
        except RSSFeed.DoesNotExist:
            params = {}
            params["message"] = f"RSS Feed with id {feed_id} does not exist"
            return Response(params, 404)

        params = {}
        status = 200
        request_data = json.loads(request.body)
        data = model_to_dict(feed_obj)
        data.update(request_data)
        feed = RSSFeedSerializer(data=data)
        if feed.is_valid() is True:
            feed_obj.__dict__.update(data)
            feed_obj.save()
            params = data
        else:
            status = 400
            params["errors"] = feed.errors
        return Response(params, status)


class RSSFeedFiltersView(APIView):
    """
    View to filter RSS feed items
        Supported methods: POST
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, feed_id):
        status = 200
        data = json.loads(request.body)
        is_read = data.get("is_read")
        
        if is_read is True:
            feed_items = FeedItemActivity.objects.filter(item__feed_id=feed_id, is_read=is_read).order_by('-item__updated_at').values_list('item__id', flat=True).distinct()
        elif is_read is False:
            feed_items = FeedItem.objects.filter(feed_id=feed_id).exclude(feed_id=feed_id, id__in=FeedItemActivity.objects.filter(is_read=not is_read).values_list('item__id', flat=True).distinct()).order_by('-updated_at')
        else:
            feed_items = FeedItem.objects.filter(feed_id=feed_id)
        
        items = []
        for item in feed_items:
            tmp_dict = model_to_dict(item)
            items.append(tmp_dict)
        return Response(items, status)


class RSSFeedsFiltersView(APIView):
    """
    View to filter RSS feed items globally
        Supported methods: POST
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        status = 200
        data = json.loads(request.body)
        is_read = data.get("is_read")
        
        if is_read is True:
            feed_items = FeedItemActivity.objects.filter(is_read=is_read).order_by('-item__updated_at').values_list('item__id', flat=True).distinct()
        elif is_read is False:
            feed_items = FeedItem.objects.exclude(id__in=FeedItemActivity.objects.filter(is_read=not is_read).values_list('item__id', flat=True).distinct()).order_by('-updated_at')
        else:
            feed_items = FeedItem.objects.all().order_by('-updated_at')
        
        items = []
        for item in feed_items:
            tmp_dict = model_to_dict(item)
            items.append(tmp_dict)
        return Response(items, status)


class RSSFeedActionView(APIView):
    """
    View to follow/unfollow/force update feeds by user
        Supported methods: POST
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, feed_id):
        params = {}
        status = 200
        data = json.loads(request.body)
        is_followed = data.get("is_followed")
        force_extract = data.get("force_extract")
        user = request.user
        feed_obj = None
        try:
            feed_obj = RSSFeed.objects.get(id=feed_id)
        except RSSFeed.DoesNotExist:
            params = {}
            params["message"] = f"RSS Feed with id {feed_id} does not exist"
            return Response(params, 404)
        
        if all(map(lambda _: _ is None, (force_extract, is_followed))):
            return Response({"error": "Please provide atleast one of - [is_followed, force_extract]"}, 400)
        
        if is_followed is not None:
            try:
                _ = RSSFeedActivity.objects.get(user=user, feed=feed_obj)
                _.is_followed = is_followed
                _.save()
            except RSSFeedActivity.DoesNotExist:
                RSSFeedActivity.objects.create(user=user, feed=feed_obj, is_followed=is_followed)
        
        if force_extract is not None:
            from src.rss.tasks import extract_rss
            extract_rss.apply_async((feed_id, feed_obj.url))
        
        return Response("OK", status)


class RSSFeedItemView(APIView):
    """
    View to get feed item
        Supported methods: GET
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, feed_id, item_id):
        # List feed item
        user = request.user
        feed_item = None
        try:
            feed_item = FeedItem.objects.get(id=item_id)
        except FeedItem.DoesNotExist:
            params = {}
            params["message"] = f"Feed item with id {item_id} does not exist"
            return Response(params, 404)
        
        feed_item_activity = None
        try:
            feed_item_activity = FeedItemActivity.objects.get(user=user, item=feed_item)
        except FeedItemActivity.DoesNotExist:
            pass
        
        tmp_dict = model_to_dict(feed_item)
        if feed_item_activity:
            feed_item_activity_dict = model_to_dict(feed_item_activity)
        tmp_dict["activity"] = feed_item_activity and feed_item_activity_dict

        return Response(tmp_dict, 200)


class RSSFeedItemActionsView(APIView):
    """
    View to mark feed item as read/unread
        Supported methods: PUT
    """

    permission_classes = (IsAuthenticated,)

    def put(self, request, feed_id, item_id):
        data = json.loads(request.body)
        user = request.user
        feed_item = None
        try:
            feed_item = FeedItem.objects.get(id=item_id)
        except FeedItem.DoesNotExist:
            params = {}
            params["message"] = f"Feed item with id {item_id} does not exist"
            return Response(params, 404)
        
        is_read = data.get("is_read")
        if is_read is None:
            return Response({"error": "Please provide one of these action in the payload - [is_read]"}, 400)

        try:
            feed_item_activity = FeedItemActivity.objects.get(user=user, item_id=item_id)
            feed_item_activity.is_read = is_read
            feed_item_activity.save()
        except FeedItemActivity.DoesNotExist:
            feed_item_activity = FeedItemActivity.objects.get_or_create(user=user, item_id=item_id, is_read=is_read)
        tmp_dict = model_to_dict(feed_item_activity)
        return Response(tmp_dict, 200)
