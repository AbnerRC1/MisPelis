from django.shortcuts import render
from django.http import HttpResponse
from movies.models import Movie

# Create your views here.
def index(request):
    saludo = "Hola mundo"
    return HttpResponse(saludo)
    
def movie(request, movie_id):
    movie = Movie.objects.get(id = movie_id)
    # pagina = f'''
    #     Titulo: {movie.title}, 
    #     Overview: {movie.overview},
    #     Genres: {[g.name for g in movie.genres.all()]}
    # '''
    context = {
        "movie": movie,
        "saludo": "welcome"
    }
    return render(request, "movies/movie.html", context=context)