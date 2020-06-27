from django.test import TestCase, Client
from django.urls import reverse
from recommendation_webapp.models import Movie,Book,Anime2

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        #Inserting sample objects in the dataset
        Movie.objects.create(Title='Goodfellas',Genre='Crime',IMDB_Score='8.7')
        Movie.objects.create(Title='Captain America',Genre='Action',IMDB_Score='6.9')
        Movie.objects.create(Title='Hangover',Genre='Comedy',IMDB_Score='7.7')

        Book.objects.create(name='Harry Potter and the Chamber of Secrects',author='J.K. Rowling',category='Science-Fiction-Fantasy-Horror',rating='4.5')
        Book.objects.create(name='Barking Up the wrong tree',author='Eric Barker',category='Personal-Development',rating='4')
        Book.objects.create(name='The Immortals of Meluha',author='Amish Tripathi',category='Mythology',rating='4.5')

        Anime2.objects.create(title='Baki',genre='action')
        Anime2.objects.create(title='Dr. Stone',genre='adventure')
        Anime2.objects.create(title='Shin-Chan',genre='comedy')

    #Home function Check
    def test_home_get(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'index.html')

#-------------------------------------------------------------------------------------------------------------

    #Quick Recommendation section function tests

    def test_all_movies_get_by_title(self):
        response = self.client.get(reverse('all_movies'),{'category':'title','search_query':'captain'})
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'all_movies.html')

    def test_all_books_get_by_author(self):
        response = self.client.get(reverse('all_books'),{'category':'author','search_query':'rowling'})
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'all_books.html')

    def test_all_animes_get_by_genre(self):
        response = self.client.get(reverse('all_animes'),{'category':'genre','search_query':'action'})
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'all_animes.html')

    #error page test
    def test_error_page_test(self):
        response = self.client.get(reverse('all_movies'),{'category':'title','search_query':'something_random'})
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'error_page.html')

#----------------------------------------------------------------------------------------------------------------

    #REcommendation Engine render test
    def test_anime_recommendation_engine_render(self):
        response = self.client.get(reverse('anime_recommendations'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'anime_recommendations.html')

    #Genre filtering tests

    def test_movie_genre_filtering(self):
        response = self.client.get(reverse('movie_genre_filtering'),{'Comedy':True,'Action':True})
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'movie_genre_filtering.html')

    def test_book_genre_filtering_with_author_and_rating(self):
        response = self.client.get(reverse('book_genre_filtering'),{'Personal-Development':True,'author':'barker','rating':True})
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'book_genre_filtering.html')

#------------------------------------------------------------------------------------------------------------------

    #Similarity filtering tests

    def test_movie_similar_filtering_render_movie_pre_filter(self):
        Movie.objects.create(Title='Hangover 2',Genre='Comedy')
        Movie.objects.create(Title='Hangover 3',Genre='Comedy')
        response = self.client.get(reverse('movie_similar_filtering'),{'movie1':'Goodfellas','movie2':'captain','movie3':'Hangover'})
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'movie_pre_filter.html')

    def test_movie_similar_filtering_without_movie_pre_filter(self):
        response = self.client.get(reverse('movie_similar_filtering'),{'movie1':'Goodfellas','movie2':'captain','movie3':'Hangover'})
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'movie_similar_filtering.html')
