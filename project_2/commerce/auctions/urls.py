from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing/", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing_page, name="listing_page"),
    path("listing/<int:listing_id>/<str:message>", views.listing_page, name="listing_page_error"),
    path("bid/<int:listing_id>", views.handle_bids, name="bids"),
    path("comment/<int:listing_id>", views.handle_comments, name="comments"),
    path("watchlist/<int:listing_id>", views.handle_watchlist, name="watchlist"),
    path("close_auction/<int:listing_id>", views.close_auction, name="close"),
    path("categories/", views.category_page, name="categories"),
    path("category/<str:category>", views.category_results, name="category"),
]

