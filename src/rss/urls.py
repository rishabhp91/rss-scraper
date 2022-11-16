# Python modules
from django.urls import path

# Local modules
from . import views


# RSS App endpoints
urlpatterns = [
    # List all feeds & Insert feed, list my feed
    path("feeds", views.RSSFeedsView.as_view(), name="feeds"),  

    # Filter read/unread feed items globally (order by date)
    path("feeds/filters", views.RSSFeedsFiltersView.as_view(), name="feeds"),  

    # Manage feed, List feed items belonging to one feed
    path("feeds/<uuid:feed_id>", views.RSSFeedView.as_view(), name="feed"),  

    # Filter read/unread feed items per feed (order by date)
    path("feeds/<uuid:feed_id>/filters", views.RSSFeedFiltersView.as_view(), name="feed"),  

    # Follow / Unfollow feeds / Force feed update
    path("feeds/<uuid:feed_id>/actions", views.RSSFeedActionView.as_view(), name="feed"),  

    # Get a feed item
    path("feeds/<uuid:feed_id>/items/<uuid:item_id>", views.RSSFeedItemView.as_view(), name="feed-item"),  

    # Mark an feed item as read/unread 
    path("feeds/<uuid:feed_id>/items/<uuid:item_id>/actions", views.RSSFeedItemActionsView.as_view(), name="feed-item"),
]
