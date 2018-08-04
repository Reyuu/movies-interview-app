from django.db import models
# Create your models here.

class Movie(models.Model):
    #to be easier on myself
    Title = models.CharField(max_length=256)
    Year = models.IntegerField() # only year
    Rated = models.CharField(max_length=10, blank=True)
    #Released = models.CharField(max_length=11, blank=True) #date fix 
    Released = models.DateField(blank=True) #date fix 
    Runtime = models.IntegerField(blank=True) # minutes
    Genre = models.CharField(max_length=256, blank=True) # separated by comma
    Director = models.CharField(max_length=128, blank=True)
    Writer = models.TextField(blank=True)
    Actors = models.TextField(blank=True)
    Plot = models.TextField(blank=True)
    Language = models.CharField(max_length=128, blank=True)
    Country = models.CharField(max_length=64, blank=True)
    Awards = models.TextField(blank=True)
    Poster = models.URLField(blank=True)
    Ratings = models.TextField(blank=True) # source:value;source:value
    Metascore = models.IntegerField(blank=True)
    imdbRating = models.FloatField(blank=True)
    imdbVotes = models.IntegerField(blank=True) # replace commas with nothing
    imdbID = models.CharField(max_length=32, blank=True)
    Type = models.CharField(max_length=16)
    #DVD = models.CharField(max_length=11, blank=True) #date fix
    DVD = models.DateField(blank=True) #date fix
    BoxOffice = models.CharField(max_length=32, blank=True)
    Production = models.CharField(max_length=64)
    Website = models.URLField(blank=True)
    Response = models.BooleanField()

class Comment(models.Model):
    movie_id = models.IntegerField()
    comment_body = models.TextField()