from django.shortcuts import render
from django.http import HttpResponse
from movies.models import Movie, MovieReview, MovieLike
from movies.forms import MovieReviewForm
from datetime import date

# Create your views here.
def index(request):
    movies = Movie.objects.all()
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