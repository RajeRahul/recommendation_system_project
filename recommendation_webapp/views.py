#Django imports for rendering html pages
from django.shortcuts import render, redirect

#importing necessary models from database
from .models import Movie, Book, Anime2

#importing Q from django to make conditional queries
from django.db.models import Q

#Home page render method
def home(request):
    if request.method == 'GET':
        return render(request,'index.html')

#quick recommendation search : Find Movies
def all_movies(request):
    search_query = request.GET.get('search_query')

    category = request.GET.get('category')

    if category == 'title':
        movie = Movie.objects.filter(Q(Title__icontains=search_query))
    if category == 'genre':
        movie = Movie.objects.filter(Q(Genre__icontains=search_query))

    #Error page check
    if movie.count() == 0 :
        return render(request,'error_page.html')

    context = {
        'movie' : movie,
        'count' : movie.count()
    }
    return render(request,'all_movies.html',context)

#quick recommendation search : Find Books
def all_books(request):
    search_query = request.GET.get('search_query')

    category = request.GET.get('category')

    if category == 'title':
        book = Book.objects.filter(Q(name__icontains=search_query))
    if category == 'genre':
        book = Book.objects.filter(Q(category__icontains=search_query))
    if category == 'author':
        book = Book.objects.filter(Q(author__icontains=search_query))
    if category == 'isbn':
        book = Book.objects.filter(Q(isbn__icontains=search_query))

    #Error page check
    if book.count() == 0:
        return render(request,'error_page.html')

    context = {
        'book' : book,
        'count' : book.count(),
    }

    return render(request,'all_books.html',context)

#quick recommendation search : Find Animes
def all_animes(request):
    search_query = request.GET.get('search_query')

    category = request.GET.get('category')

    if category == 'title':
        anime = Anime2.objects.filter(Q(title__icontains=search_query))
    if category == 'genre':
        anime = Anime2.objects.filter(Q(genre__icontains=search_query))

    #Error page check
    if anime.count() == 0:
        return render(request,'error_page.html')

    context = {
        'anime' : anime,
        'count' : anime.count(),
    }

    return render(request,'all_animes.html',context)

#Some common methods defined that can be directly accessed in the main filtering methods
#---------------------------------------------------------------------------------------

def Average(lst):
    return sum(lst) / len(lst)

def CommonCategories(category_list1, category_list2, category_list3):

    unique_categories = []

    for i in category_list1:
        if i not in unique_categories:
            unique_categories.append(i)
    for i in category_list2:
        if i not in unique_categories:
            unique_categories.append(i)
    for i in category_list3:
        if i not in unique_categories:
            unique_categories.append(i)

    return unique_categories

def Find_Average_Rating(rating1,rating2,rating3):
    list1 = []
    list2 = []
    list3 = []
    lst = []

    for i in rating1:
        list1.append(float(i))
    for i in rating2:
        list2.append(float(i))
    for i in rating3:
        list3.append(float(i))

    lst.append(round(Average(list1),1))
    lst.append(round(Average(list2),1))
    lst.append(round(Average(list3),1))

    return round(Average(lst),1)

def movie_categories(genre1,genre2,genre3):
    list = []
    unique_list = []

    for i in genre1:
        list.append(i.split('|'))
    for i in genre2:
        list.append(i.split('|'))
    for i in genre3:
        list.append(i.split('|'))

    for i in range(len(list)):
        for j in list[i]:
            if j not in unique_list:
                unique_list.append(j)

    return unique_list

def anime_categories(genre1,genre2,genre3):
    list = []
    unique_list = []

    for i in genre1:
        list.append(i.split(', '))
    for i in genre2:
        list.append(i.split(', '))
    for i in genre3:
        list.append(i.split(', '))

    for i in range(len(list)):
        for j in list[i]:
            if j not in unique_list:
                unique_list.append(j)

    return unique_list

#---------------------------------------------------------------------------------------

#Movie recommendation engine rendering method
def movie_recommendations(request):

    list = ['Animation','Adventure','Drama','Music','Fantasy','Thriller','Comedy','Sci-Fi','Horror','Action','Romance',
            'Documentary','Family','Biography','War','Crime','Sport','Mystery']

    return render(request,'movie_recommendations.html',{'list':list})

#Movie Genre based recommendations
def movie_genre_filtering(request):

    list = ['Animation','Adventure','Drama','Music','Fantasy','Thriller','Comedy','Sci-Fi','Horror','Action','Romance',
            'Documentary','Family','Biography','War','Crime','Sport','Mystery']

    genre_list = []

    for i in list:
        if request.GET.get(i):
            genre_list.append(str(i))

    test_list = []

    if request.GET.get('rating'):
        for i in range(len(genre_list)):
            test_list.append(Movie.objects.filter(Q(Genre__startswith=genre_list[i]),Q(IMDB_Score__gte=7)))
    else:
        for i in range(len(genre_list)):
            test_list.append(Movie.objects.filter(Q(Genre__startswith=genre_list[i])))

    #Error page check
    if not test_list:
        return render(request,'error_page.html')

    context = {
        'test_list' : test_list,
        'genre_list' : genre_list
    }

    return render(request,'movie_genre_filtering.html',context)

#Movie similarity filtering method 1
def movie_similar_filtering(request):

    movie1 = request.GET.get('movie1')
    movie2 = request.GET.get('movie2')
    movie3 = request.GET.get('movie3')

    #Error page check
    mov1 = Movie.objects.filter(Q(Title__icontains=movie1))
    mov2 = Movie.objects.filter(Q(Title__icontains=movie2))
    mov3 = Movie.objects.filter(Q(Title__icontains=movie3))

    if mov1.count() == 0 or mov2.count() == 0 or mov3.count() == 0:
        return render(request,'error_page.html')

    if mov1.count() > 1 or mov2.count() > 1 or mov3.count() > 1:
        context = {
            'movie1' : movie1,
            'movie2' : movie2,
            'movie3' : movie3,
            'mov1' : mov1,
            'mov2' : mov2,
            'mov3' : mov3
        }
        return render(request,'movie_pre_filter.html',context)

    score1 = Movie.objects.filter(Q(Title__icontains=movie1)).values_list('IMDB_Score',flat=True)
    score2 = Movie.objects.filter(Q(Title__icontains=movie2)).values_list('IMDB_Score',flat=True)
    score3 = Movie.objects.filter(Q(Title__icontains=movie3)).values_list('IMDB_Score',flat=True)

    genre1 = Movie.objects.filter(Q(Title__icontains=movie1)).values_list('Genre',flat=True)
    genre2 = Movie.objects.filter(Q(Title__icontains=movie2)).values_list('Genre',flat=True)
    genre3 = Movie.objects.filter(Q(Title__icontains=movie3)).values_list('Genre',flat=True)

    avg = Find_Average_Rating(score1,score2,score3)

    imdb_score = str(float(avg) - 1)

    genre_list_final = CommonCategories(genre1,genre2,genre3)
    genre_list = movie_categories(genre1, genre2, genre3)

    test_list = []

    for i in range(len(genre_list)):
        test_list.append(Movie.objects.filter(Q(Genre__startswith=genre_list[i])))

    movie = Movie.objects.filter(Q(Genre__in=genre_list_final))

    context = {
        'imdb_score' : imdb_score,
        'avg' : avg,
        'movie' : movie,
        'genre_list_final' : genre_list,
        'test_list' : test_list
    }

    return render(request,'movie_similar_filtering.html',context)

#Movie similarity filtering method 2
def movie_pre_filter(request):
    mov1 = request.GET.getlist('movie1')[0]
    mov2 = request.GET.getlist('movie2')[0]
    mov3 = request.GET.getlist('movie3')[0]

    score1 = Movie.objects.filter(Q(imdbId__exact=mov1)).values_list('IMDB_Score',flat=True)
    score2 = Movie.objects.filter(Q(imdbId__exact=mov2)).values_list('IMDB_Score',flat=True)
    score3 = Movie.objects.filter(Q(imdbId__exact=mov3)).values_list('IMDB_Score',flat=True)

    genre1 = Movie.objects.filter(Q(imdbId__exact=mov1)).values_list('Genre',flat=True)
    genre2 = Movie.objects.filter(Q(imdbId__exact=mov2)).values_list('Genre',flat=True)
    genre3 = Movie.objects.filter(Q(imdbId__exact=mov3)).values_list('Genre',flat=True)

    avg = Find_Average_Rating(score1,score2,score3)

    imdb_score = str(float(avg) - 1)

    genre_list_final = CommonCategories(genre1,genre2,genre3)
    genre_list = movie_categories(genre1, genre2, genre3)

    test_list = []

    for i in range(len(genre_list)):
        test_list.append(Movie.objects.filter(Q(Genre__startswith=genre_list[i])))

    movie = Movie.objects.filter(Q(Genre__in=genre_list_final))

    context = {
        'imdb_score' : imdb_score,
        'avg' : avg,
        'movie' : movie,
        'genre_list_final' : genre_list,
        'test_list' : test_list
    }

    return render(request,'movie_similar_filtering.html',context)

#Book recommendation engine rendering method
def book_recommendations(request):
    list = ['Medical','Science-Geography','Health','History-Archaeology','Art-Photography','Garden','Biography','Humour',
            'Business-Finance-Law','Mind-Body-Spirit','Childrens-Books','Personal-Development','Computing','Poetry-Drama','Crafts-Hobbies',
            'Religion','Crime-Thriller','Romance','Entertainment','Science-Fiction-Fantasy-Horror','Food-Drink','Graphic-Novels-Anime-Manga',
            'Society-Social-Sciences','Sport','Technology-Engineering','Teen-Young-Adult','Travel-Holiday-Guides']

    context = {
        'list' : list,
    }

    return render(request,'book_recommendations.html',context)

#Book genre based recommendations
def book_genre_filtering(request):

    list = ['Medical','Science-Geography','Health','History-Archaeology','Art-Photography','Garden','Biography','Humour',
            'Business-Finance-Law','Mind-Body-Spirit','Childrens-Books','Personal-Development','Computing','Poetry-Drama','Crafts-Hobbies',
            'Religion','Crime-Thriller','Romance','Entertainment','Science-Fiction-Fantasy-Horror','Food-Drink','Graphic-Novels-Anime-Manga',
            'Society-Social-Sciences','Sport','Technology-Engineering','Teen-Young-Adult','Travel-Holiday-Guides']

    category_list = []

    for i in list:
        if request.GET.get(i):
            category_list.append(str(i))

    author = request.GET.get('author')

    if request.GET.get('rating') and author != '':
        book = Book.objects.filter(Q(category__in=category_list),Q(rating__gte=4),Q(author__icontains=author))
    elif request.GET.get('rating') and author == '':
        book = Book.objects.filter(Q(category__in=category_list),Q(rating__gte=4))
    elif request.GET.get('rating') != 'on' and author != '':
        book = Book.objects.filter(Q(category__in=category_list),Q(author__icontains=author))
    else :
        book = Book.objects.filter(Q(category__in=category_list))

    #Error page check
    if book.count() == 0:
        return render(request,'error_page.html')

    context = {
        'book' : book,
        'genre_list' : category_list
    }

    return render(request,'book_genre_filtering.html',context)

#book similarity filtering method 1
def book_similar_filtering(request):

    book1 = request.GET.get('book1')
    book2 = request.GET.get('book2')
    book3 = request.GET.get('book3')

    #Error page check
    b1 = Book.objects.filter(Q(name__icontains=book1))
    b2 = Book.objects.filter(Q(name__icontains=book2))
    b3 = Book.objects.filter(Q(name__icontains=book3))

    if b1.count() == 0 or b2.count() == 0 or b3.count() == 0:
        return render(request,'error_page.html')

    if b1.count() > 1 or b2.count() > 1 or b3.count() > 1:
        context = {
            'book1' : book1,
            'book2' : book2,
            'book3' : book3,
            'b1' : b1,
            'b2' : b2,
            'b3' : b3
        }
        return render(request,'book_pre_filter.html',context)

    rating1 = Book.objects.filter(Q(name__icontains=book1)).values_list('rating',flat=True)
    rating2 = Book.objects.filter(Q(name__icontains=book2)).values_list('rating',flat=True)
    rating3 = Book.objects.filter(Q(name__icontains=book3)).values_list('rating',flat=True)

    category1 = Book.objects.filter(Q(name__icontains=book1)).values_list('category',flat=True)
    category2 = Book.objects.filter(Q(name__icontains=book2)).values_list('category',flat=True)
    category3 = Book.objects.filter(Q(name__icontains=book3)).values_list('category',flat=True)

    author1 = Book.objects.filter(Q(name__icontains=book1)).values_list('author',flat=True)
    author2 = Book.objects.filter(Q(name__icontains=book2)).values_list('author',flat=True)
    author3 = Book.objects.filter(Q(name__icontains=book3)).values_list('author',flat=True)

    avg = Find_Average_Rating(rating1,rating2,rating3)

    score = str(float(avg) - 0.5)

    category_list_final = CommonCategories(category1, category2, category3)
    author_list_final = CommonCategories(author1,author2,author3)

    book = Book.objects.filter(Q(category__in=category_list_final)|Q(author__in=author_list_final))

    context = {
        'category_list_final' : category_list_final,
        'author_list_final' : author_list_final,
        'book' : book,
        'avg' : avg,
        'score' : score,
    }

    return render(request,'book_similar_filtering.html',context)

#book similarity filtering method 2
def book_pre_filter(request):
    b1 = request.GET.getlist('book1')[0]
    b2 = request.GET.getlist('book2')[0]
    b3 = request.GET.getlist('book3')[0]

    rating1 = Book.objects.filter(Q(isbn__exact=b1)).values_list('rating',flat=True)
    rating2 = Book.objects.filter(Q(isbn__exact=b2)).values_list('rating',flat=True)
    rating3 = Book.objects.filter(Q(isbn__exact=b3)).values_list('rating',flat=True)

    category1 = Book.objects.filter(Q(isbn__exact=b1)).values_list('category',flat=True)
    category2 = Book.objects.filter(Q(isbn__exact=b2)).values_list('category',flat=True)
    category3 = Book.objects.filter(Q(isbn__exact=b3)).values_list('category',flat=True)

    author1 = Book.objects.filter(Q(isbn__exact=b1)).values_list('author',flat=True)
    author2 = Book.objects.filter(Q(isbn__exact=b2)).values_list('author',flat=True)
    author3 = Book.objects.filter(Q(isbn__exact=b3)).values_list('author',flat=True)

    avg = Find_Average_Rating(rating1,rating2,rating3)

    score = str(float(avg) - 0.5)

    category_list_final = CommonCategories(category1, category2, category3)
    author_list_final = CommonCategories(author1,author2,author3)

    book = Book.objects.filter(Q(category__in=category_list_final)|Q(author__in=author_list_final))

    context = {
        'category_list_final' : category_list_final,
        'author_list_final' : author_list_final,
        'book' : book,
        'avg' : avg,
        'score' : score,
    }

    return render(request,'book_similar_filtering.html',context)

#Anime recommendation engine rendering method
def anime_recommendations(request):

    list = ['Action','Adventure','Comedy','Mystery','Magic','Supernatural','Sports','School','Drama','Psychological','Kids','Romance','Fantasy']

    context = {
        'list' : list,
    }

    return render(request,'anime_recommendations.html',context)

#anime genre based recommendations
def anime_genre_filtering(request):

    list = ['Action','Adventure','Comedy','Mystery','Magic','Supernatural','Sports','School','Drama','Psychological','Kids','Romance','Fantasy']

    genre_list = []

    for i in list:
        if request.GET.get(i):
            genre_list.append(str(i))

    test_list = []

    if request.GET.get('rating'):
        for i in range(len(genre_list)):
            test_list.append(Anime2.objects.filter(Q(genre__startswith=genre_list[i]),Q(score__gte=7)))
    else:
        for i in range(len(genre_list)):
            test_list.append(Anime2.objects.filter(Q(genre__startswith=genre_list[i])))

    #Error page check
    if not test_list:
        return render(request,'error_page.html')

    context = {
        'test_list' : test_list,
        'genre_list' : genre_list

    }

    return render(request,'anime_genre_filtering.html',context)

#anime similarity filtering method 1
def anime_similar_filtering(request):

    anime1 = request.GET.get('anime1')
    anime2 = request.GET.get('anime2')
    anime3 = request.GET.get('anime3')

    #Error page check
    a1 = Anime2.objects.filter(Q(title__icontains=anime1))
    a2 = Anime2.objects.filter(Q(title__icontains=anime2))
    a3 = Anime2.objects.filter(Q(title__icontains=anime3))

    if a1.count() == 0 or a2.count() == 0 or a3.count() == 0:
        return render(request,'error_page.html')

    if a1.count() > 1 or a2.count() > 1 or a3.count() > 1:
        context = {
            'anime1' : anime1,
            'anime2' : anime2,
            'anime3' : anime3,
            'a1' : a1,
            'a2' : a2,
            'a3' : a3
        }
        return render(request,'anime_pre_filter.html',context)

    score1 = Anime2.objects.filter(Q(title__icontains=anime1)).values_list('score',flat=True)
    score2 = Anime2.objects.filter(Q(title__icontains=anime2)).values_list('score',flat=True)
    score3 = Anime2.objects.filter(Q(title__icontains=anime3)).values_list('score',flat=True)

    genre1 = Anime2.objects.filter(Q(title__icontains=anime1)).values_list('genre',flat=True)
    genre2 = Anime2.objects.filter(Q(title__icontains=anime2)).values_list('genre',flat=True)
    genre3 = Anime2.objects.filter(Q(title__icontains=anime3)).values_list('genre',flat=True)

    avg = Find_Average_Rating(score1,score2,score3)

    score = str(float(avg) - 1)

    genre_list_final = CommonCategories(genre1,genre2,genre3)
    genre_list = anime_categories(genre1, genre2, genre3)

    test_list = []

    for i in range(len(genre_list)):
        test_list.append(Anime2.objects.filter(Q(genre__startswith=genre_list[i])))

    anime = Anime2.objects.filter(Q(genre__in=genre_list_final))

    context = {
        'score' : score,
        'avg' : avg,
        'anime' : anime,
        'genre_list_final' : genre_list,
        'test_list' : test_list
    }

    return render(request,'anime_similar_filtering.html',context)

#anime similarity filtering method 2
def anime_pre_filter(request):

    a1 = request.GET.getlist('anime1')[0]
    a2 = request.GET.getlist('anime2')[0]
    a3 = request.GET.getlist('anime3')[0]

    score1 = Anime2.objects.filter(Q(uid__exact=a1)).values_list('score',flat=True)
    score2 = Anime2.objects.filter(Q(uid__exact=a2)).values_list('score',flat=True)
    score3 = Anime2.objects.filter(Q(uid__exact=a3)).values_list('score',flat=True)

    genre1 = Anime2.objects.filter(Q(uid__exact=a1)).values_list('genre',flat=True)
    genre2 = Anime2.objects.filter(Q(uid__exact=a2)).values_list('genre',flat=True)
    genre3 = Anime2.objects.filter(Q(uid__exact=a3)).values_list('genre',flat=True)

    avg = Find_Average_Rating(score1,score2,score3)

    score = str(float(avg) - 1)

    genre_list_final = CommonCategories(genre1,genre2,genre3)
    genre_list = anime_categories(genre1, genre2, genre3)

    test_list = []

    for i in range(len(genre_list)):
        test_list.append(Anime2.objects.filter(Q(genre__startswith=genre_list[i])))

    anime = Anime2.objects.filter(Q(genre__in=genre_list_final))

    context = {
        'score' : score,
        'avg' : avg,
        'anime' : anime,
        'genre_list_final' : genre_list,
        'test_list' : test_list
    }

    return render(request,'anime_similar_filtering.html',context)
