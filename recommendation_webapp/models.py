from djongo import models #used djongo to connect to Mongodb

class Movie(models.Model):
    imdbId = models.CharField(max_length = 10, null=True)
    Imdb_Link = models.CharField(max_length = 500, null=True)
    Title = models.CharField(max_length = 500, null=True)
    IMDB_Score = models.CharField(max_length = 500, null=True)
    Genre = models.CharField(max_length = 500, null=True)
    Poster = models.TextField()

    def __str__(self):
        return f'{self.Title}'

class Book(models.Model):
    image = models.TextField()
    name = models.CharField(max_length = 500, null=True)
    author = models.CharField(max_length = 500, null=True)
    rating = models.CharField(max_length = 500, null=True)
    isbn = models.CharField(max_length = 500, null=True)
    category = models.CharField(max_length = 500, null=True)
    img_paths = models.CharField(max_length = 500, null=True)
    link = models.TextField()

    def __str__(self):
        return f'{self.name}'

class Anime2(models.Model):
    uid = models.CharField(max_length = 500, null=True)
    title = models.CharField(max_length = 500, null=True)
    synopsis = models.TextField()
    genre = models.CharField(max_length = 500, null=True)
    aired = models.CharField(max_length = 500, null=True)
    episodes = models.CharField(max_length = 500, null=True)
    members = models.CharField(max_length = 500, null=True)
    popularity = models.CharField(max_length = 500, null=True)
    ranked = models.CharField(max_length = 500, null=True)
    score = models.CharField(max_length = 500, null=True)
    img_url = models.TextField()
    link = models.TextField()

    def __str__(self):
        return f'{self.title}'
