from django.shortcuts import render, redirect
from .models import Movie, Book, Anime2
from django.db.models import Q

def home(request):
    if request.method == 'GET':
        return render(request,'index.html')

def all_movies(request):
    number_list = ['1','2','3','4','5','6','7','8','9','0']

    search_query = request.GET.get('search_query')

    category = request.GET.get('category')

    if category == 'title':
        movie = Movie.objects.filter(Q(Title__icontains=search_query) ,Q(Title__icontains=number_list))
    if category == 'genre':
        movie = Movie.objects.filter(Q(Genre__icontains=search_query))

    if movie.count() == 0 :
        return render(request,'error_page.html')

    context = {
        'movie' : movie,
        'count' : movie.count(),
        'string' : " Objects Found",
    }
    return render(request,'all_movies.html',context)

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

    if book.count() == 0:
        return render(request,'error_page.html')

    context = {
        'book' : book,
        'count' : book.count(),
        'string' : " Objects Found",
    }

    return render(request,'all_books.html',context)

def all_animes(request):
    search_query = request.GET.get('search_query')

    category = request.GET.get('category')

    if category == 'title':
        anime = Anime2.objects.filter(Q(title__icontains=search_query))
    if category == 'genre':
        anime = Anime2.objects.filter(Q(genre__icontains=search_query))

    if anime.count() == 0:
        return render(request,'error_page.html')

    context = {
        'anime' : anime,
        'count' : anime.count(),
        'string' : " Objects Found"
    }

    return render(request,'all_animes.html',context)

def Average(lst):
    return sum(lst) / len(lst)

def CommonCategories(category1, category2, category3):

    category_list1 = []
    category_list2 = []
    category_list3 = []
    unique_categories = []

    for i in category1:
        category_list1.append(i)
    for i in category2:
        category_list1.append(i)
    for i in category3:
        category_list1.append(i)

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

def movie_recommendations(request):

    list = ['Animation','Adventure','Drama','Music','Fantasy','Thriller','Comedy','Sci-Fi','Horror','Action','Romance',
            'Documentary','Family','Biography','War','Crime','Sport','Mystery']

    return render(request,'movie_recommendations.html',{'list':list})

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

    context = {
        'test_list' : test_list,
        'genre_list' : genre_list
    }

    return render(request,'movie_genre_filtering.html',context)


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

    score1 = Movie.objects.filter(Q(Title__icontains=movie1)).values_list('IMDB_Score',flat=True)
    score2 = Movie.objects.filter(Q(Title__icontains=movie2)).values_list('IMDB_Score',flat=True)
    score3 = Movie.objects.filter(Q(Title__icontains=movie3)).values_list('IMDB_Score',flat=True)

    genre1 = Movie.objects.filter(Q(Title__icontains=movie1)).values_list('Genre',flat=True)
    genre2 = Movie.objects.filter(Q(Title__icontains=movie2)).values_list('Genre',flat=True)
    genre3 = Movie.objects.filter(Q(Title__icontains=movie3)).values_list('Genre',flat=True)

    avg = Find_Average_Rating(score1,score2,score3)

    imdb_score = str(float(avg) - 1)

    genre_list_final = CommonCategories(genre1, genre2, genre3)

    movie = Movie.objects.filter(Q(Genre__in=genre_list_final))

    context = {
        'imdb_score' : imdb_score,
        'avg' : avg,
        'movie' : movie,
        'genre_list_final' : genre_list_final
    }

    return render(request,'movie_similar_filtering.html',context)

def book_recommendations(request):
    list = ['Medical','Science-Geography','Health','History-Archeology','Art-Photography','Garden','Biography','Humour',
            'Business-Finance-Law','Mind-Body-Spirit','Childrens-Books','Personal-Development','Computing','Poetry-Drama','Crafts-Hobbies',
            'Religion','Crime-Thriller','Romance','Entertainment','Science-Fiction-Fantasy-Horror','Food-Drink','Graphic-Novels-Anime-Manga',
            'Society-Social-Sciences','Sport','Technology-Engineering','Teen-Young-Adult','Travel-Holiday-Guides']

    context = {
        'list' : list,
    }

    return render(request,'book_recommendations.html',context)

def book_genre_filtering(request):

    list = ['Medical','Science-Geography','Health','History-Archeology','Art-Photography','Garden','Biography','Humour',
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

    if book.count() == 0:
        return render(request,'error_page.html')

    context = {
        'book' : book,
        'genre_list' : category_list
    }

    return render(request,'book_genre_filtering.html',context)

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

def anime_recommendations(request):

    list = ['Action','Adventure','Comedy','Mystery','Magic','Supernatural','Sports','School','Drama','Psychological','Kids','Romance','Fantasy']

    context = {
        'list' : list,
    }

    return render(request,'anime_recommendations.html',context)

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

    context = {
        'test_list' : test_list,
        'genre_list' : genre_list

    }

    return render(request,'anime_genre_filtering.html',context)

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

    score1 = Anime2.objects.filter(Q(title__icontains=anime1)).values_list('score',flat=True)
    score2 = Anime2.objects.filter(Q(title__icontains=anime2)).values_list('score',flat=True)
    score3 = Anime2.objects.filter(Q(title__icontains=anime3)).values_list('score',flat=True)

    genre1 = Anime2.objects.filter(Q(title__icontains=anime1)).values_list('genre',flat=True)
    genre2 = Anime2.objects.filter(Q(title__icontains=anime2)).values_list('genre',flat=True)
    genre3 = Anime2.objects.filter(Q(title__icontains=anime3)).values_list('genre',flat=True)

    avg = Find_Average_Rating(score1,score2,score3)

    score = str(float(avg) - 1)

    genre_list_final = CommonCategories(genre1, genre2, genre3)

    anime = Anime2.objects.filter(Q(genre__in=genre_list_final))

    context = {
        'score' : score,
        'avg' : avg,
        'anime' : anime,
        'genre_list_final' : genre_list_final
    }

    return render(request,'anime_similar_filtering.html',context)
