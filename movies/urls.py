from django.urls import path
from .views import *

urlpatterns = [
    path('<int:movie_id>/', movie),
    path('movie_review/add/<int:movie_id>/', add_review),
    path('like/<int:movie_id>/', add_like),
    path('movie_reviews/<int:movie_id>/', movie_reviews, name='movie_reviews'),
    path('about/', about),
    path('mymovies/<int:users_id>/', my_movies),
    path("search/", search_movies, name="search_movies"),
    path("random/", random_movies, name="random_movies"),
    path("recommended/<int:movie_id>/", recommended_movies, name="random_movies"),
    path('', index)
]