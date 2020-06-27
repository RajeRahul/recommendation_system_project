from django.test import SimpleTestCase
from django.urls import reverse, resolve
from recommendation_webapp.views import home, all_movies, book_recommendations, anime_similar_filtering, movie_pre_filter

class TestUrls(SimpleTestCase):

    #Home Url Test
    def test_home_url(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    #Movie Quick Search Url test
    def test_all_movies_url(self):
        url = reverse('all_movies')
        self.assertEquals(resolve(url).func, all_movies)

    #Book recommendation Engine url test
    def test_book_recommendations_url(self):
        url = reverse('book_recommendations')
        self.assertEquals(resolve(url).func, book_recommendations)

    #Anime similarity filtering url test
    def test_anime_similar_filtering_url(self):
        url = reverse('anime_similar_filtering')
        self.assertEquals(resolve(url).func, anime_similar_filtering)

    #Movie pre filter url test
    def test_movie_pre_filter_url(self):
        url = reverse('movie_pre_filter')
        self.assertEquals(resolve(url).func, movie_pre_filter)
