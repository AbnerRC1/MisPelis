from django.contrib import admin
from movies.models import Movie, Genre, Job, Person, MovieCredit, MovieReview, MovieLike

# Register your models here.
admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Job)
admin.site.register(Person)
admin.site.register(MovieCredit)
admin.site.register(MovieReview)
admin.site.register(MovieLike)