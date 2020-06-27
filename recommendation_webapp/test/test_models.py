from django.test import TestCase, Client
from recommendation_webapp.models import Movie,Anime2,Book

class TestModels(TestCase):

    #Test the Movie model
    def test_Movie_model(self):
        movie = Movie.objects.create(Title='Fight Club',Genre='Crime',IMDB_Score='8.7')
        max_length = Movie._meta.get_field('Title').max_length
        self.assertEquals(max_length, 500)
        self.assertEquals(str(movie),'Fight Club')

    #Test the Book model
    def test_Book_model(self):
        book = Book.objects.create(name='Harry Potter and the Chamber of Secrects',author='J.K. Rowling',category='Science-Fiction-Fantasy-Horror')
        max_length = Book._meta.get_field('name').max_length
        self.assertEquals(max_length, 500)
        self.assertEquals(str(book),'Harry Potter and the Chamber of Secrects')

    #Test the Anime2 model
    def test_Anime2_model(self):
        anime = Anime2.objects.create(title='Dragon Ball',genre='action')
        max_length = Anime2._meta.get_field('title').max_length
        self.assertEquals(max_length, 500)
        self.assertEquals(str(anime),'Dragon Ball')
