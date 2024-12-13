from django.shortcuts import render
from django.http import HttpResponse
from movies.models import Movie, MovieReview
from movies.forms import MovieReviewForm
from datetime import date
from django.core.paginator import Paginator
from django.contrib.postgres import search
from django.contrib.auth import get_user_model
import random

# Create your views here.
def index(request):
    movies = list(Movie.objects.all())
    random_movies = []
    users = get_user_model().objects.all()
    print(users)
    if movies:
        random_movies= random.sample(movies,4)
    return render(request,'movies/index.html', {'movies': random_movies, 'users':users} )
    
def my_movies(request, users_id):
    movies = Movie.objects.all()
    selected_ids = []
    
    for movie in movies:
        id = movie.id
        reviewed_movie = MovieReview.objects.all().filter(user_id=users_id).values('movie_id').filter(movie_id=id)
        if reviewed_movie: selected_ids.append(reviewed_movie[0]['movie_id'])

    movies = movies.filter(id__in=selected_ids)
    
    context = { 'movies':movies, 'message':'welcome' }
    return render(request,'movies/index.html', context=context )

def movie(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    review_form = MovieReviewForm()
    context = { 'movie':movie, 'saludo':'welcome', "review_form":review_form }
    return render(request,'movies/movie.html', context=context )
    
def add_review(request, movie_id):
    form = None
    movie = Movie.objects.get(id=movie_id)
    if request.method == 'POST':
        form = MovieReviewForm(request.POST)
        left_review_already = MovieReview.objects.all().filter(user_id=request.user.id).values('movie_id').filter(movie_id=movie_id)
        if left_review_already:
            return render(request,
                  'movies/error_modal.html',
                  {'error_description': 'Ya creó una reseña para esta película anteriormente. Por favor intente con otra película o cuenta de usuario'})
        if form.is_valid():
            rating = form.cleaned_data['rating']
            title  = form.cleaned_data['title']
            review = form.cleaned_data['review']
            movie_review = MovieReview(
                    movie=movie,
                    rating=rating,
                    title=title,
                    review=review,
                    user=request.user,
                    date=date.today().strftime("%d/%m/%Y"))
            movie_review.save()
            return HttpResponse(status=204,
                                headers={'HX-Trigger': 'listChanged'})
        else:
            return render(request,
                  'movies/error_modal.html',
                  {'error_description': 'El formulario no es válido. Por favor intente denuevo'})
    else:
        form = MovieReviewForm()
        return render(request,
                  'movies/movie_review_form.html',
                  {'movie_review_form': form, 'movie':movie})
                  
def movie_reviews(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    return render(request,'movies/reviews.html', context={'movie':movie } )
    
def about(request):
    return render(request,'movies/about.html' )
    
def add_like(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    movie.likes += 1
    movie.save()
        
    review_form = MovieReviewForm()
    context = { 'movie':movie, 'saludo':'welcome', "review_form":review_form }
    return render(request,'movies/movie.html', context=context )

def search_movies(request):
    if request.method == 'GET':
        value = request.GET['search']
        movies = ft_movies(value)

        paginator = Paginator(movies, 4)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, 'movies/movies_search.html',
                      {'movies': movies, 'search_value': value,
                       "page_obj": page_obj})
    else:
        return render(request, 'movies/index.html',
                      {'movies': [], 'search_value': None})


def ft_movies(value):
    vector = (
        search.SearchVector("title", weight="A")
    )
    query = search.SearchQuery(value, search_type="websearch")
    return (
        Movie.objects.annotate(
            search=vector,
            rank=search.SearchRank(vector, query),
        )
        .filter(search=query)
        .order_by("-rank")
    )
    
def random_movies(request):
    movies = list(Movie.objects.all())
    random_movies = []
    if movies:
        random_movies = random.sample(movies, 4)
    return render(request, 'movies/movies_random.html',
                  {'movies': random_movies})
    
def recommended_movies(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    recommended_genres = []
    for genre in movie.genres.all():
        recommended_genres.append(genre)
    
    movies = list(Movie.objects.all())
    recommended_movies = []
    target_select = 4
    random.shuffle(movies)
    for movie in movies:
        if movie.id != movie_id:
            for genre in movie.genres.all():
                for recommended_genre in recommended_genres:
                    if genre == recommended_genre and target_select != 0:
                        target_select -= 1
                        recommended_movies.append(movie)
                        print(f"yes for {movie}, is now {target_select}")
                        break
                    break
            else:
                continue
            break
    
    if target_select != 0:
        recommended_movies.append(random.sample(movies, target_select)[0])
        
    print(recommended_movies)
    return render(request, 'movies/movies_random.html',
                  {'movies': recommended_movies})