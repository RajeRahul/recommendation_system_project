"""recommendation_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from recommendation_webapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recommendations_webapp_home/',views.home,name='home'),
    path('all_movies/',views.all_movies,name='all_movies'),
    path('all_books/',views.all_books,name='all_books'),
    path('all_animes/',views.all_animes,name='all_animes'),
    path('movie_recommendations/',views.movie_recommendations,name='movie_recommendations'),
    path('movie_genre_filtering',views.movie_genre_filtering,name='movie_genre_filtering'),
    path('movie_similar_filtering/',views.movie_similar_filtering,name='movie_similar_filtering'),
    path('book_recommendations/',views.book_recommendations,name='book_recommendations'),
    path('book_genre_filtering',views.book_genre_filtering,name='book_genre_filtering'),
    path('book_similar_filtering/',views.book_similar_filtering,name='book_similar_filtering'),
    path('anime_recommendations/',views.anime_recommendations,name='anime_recommendations'),
    path('anime_genre_filtering',views.anime_genre_filtering,name='anime_genre_filtering'),
    path('anime_similar_filtering/',views.anime_similar_filtering,name='anime_similar_filtering'),
    path('movie_pre_filter/',views.movie_pre_filter,name='movie_pre_filter'),
    path('book_pre_filter/',views.book_pre_filter,name='book_pre_filter'),
    path('anime_pre_filter/',views.anime_pre_filter,name='anime_pre_filter'),
]
