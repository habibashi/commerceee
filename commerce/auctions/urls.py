from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("CreateList", views.CreateList, name="CreateList"),
    path("categories", views.categories, name="categories"),
    path("view/<int:listing_id>", views.view, name="view"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("delete/<int:delete_id>", views.delete, name="delete"),
    path("addwatchlist/<int:listing_id>", views.addwatchlist, name="addwatchlist"),
    path("bids/<int:listing_id>", views.bids, name="bids"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("End/<int:listing_id>", views.End, name="End")
    # path("addcomment/<int:listing_id>", views.addcomment, name="addcomment")
    # path("count/<int:count_id>", views.count, name="count")
]
