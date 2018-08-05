from requests import get as rget
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from movies.models import Movie, Comment
from movies.serializers import MovieSerializer, CommentSerializer
from intapi.settings import OMDBAPI_KEY
from datetime import datetime
# Create your views here.

@csrf_exempt
def comment(request):
    """
    /comments
        POST /comments
        @param `movie_id` required
        @param `comment` required
        save to db
        @response (return comment)

        GET /comments
        @param `movie_id` optional
        @response fetch all comments, `movie_id` filtered if present
    """
    if request.method == "POST":
        movie_id = request.POST.get("movie_id", "")
        comment = request.POST.get("comment", "")
        #check if any POST argument is empty
        if (movie_id == "") or (comment == ""):
            return JsonResponse({"error": "empty argument"}, status=400)
        #check if movie exists in database
        entry = Movie.objects.filter(id=movie_id)
        if not(entry.exists()):
            return JsonResponse({"error": "movie not found in database"}, status=400)
        #create new Comment object
        cmnt = Comment(movie_id=movie_id, comment_body=comment)
        #commit to database
        cmnt.save()
        #serialize what you got
        serialized_cmnt = CommentSerializer(cmnt)
        #return it
        return JsonResponse(serialized_cmnt.data, status=201)

    if request.method == "GET":
        movie_id = request.GET.get("movie_id", "")
        #get all comments
        all_comments = Comment.objects.all()
        #if movie_id is not empty filter them
        if not(movie_id == ""):
            all_comments = all_comments.filter(movie_id=movie_id)
        #serialize what you got
        serialized_all = CommentSerializer(all_comments, many=True)
        #return it
        return JsonResponse(serialized_all.data, status=201, safe=False)

def get_movie(title):
    #get movie data from API by get 
    url = "http://www.omdbapi.com/"
    params = {"apikey": OMDBAPI_KEY, "t": title}
    r = rget(url, params=params)
    movie = r.json()
    return movie

@csrf_exempt
def movie(request):
    """
    /movies
        POST /movies
        @param `title` required validated
        fetch details from omdbapi.com and save to DB
        @response (
            full movie object,
            data fetched from API
            )

        GET /movies
        fetch list of all movies present (be smart) <serializer>(<queryset>, many=True)
    """
    if request.method == "POST":
        title = request.POST.get("title", "")
        #if title is blank space return error
        if title == "":
            return JsonResponse({"error": "no title"}, status=400)
        #get movie
        movie = get_movie(title)
        #check if already in database
        entry = Movie.objects.filter(Title__iexact=movie["Title"])
        if entry.exists():
            return JsonResponse({"error": "already in database, use GET"}, status=400)
        #response could fail
        if movie["Response"] == "False": # in what universe would you do this
            return JsonResponse({"error": movie["Error"].lower()})
        #we only care for movies
        if not(movie["Type"] == "movie"):
            return JsonResponse({"error": "not a movie"}, status=400)
        #copy original movie object (tfw 2018 and still have to use tricks to duplicate variable)
        org_movie = dict(movie)
        #check if anywhere is N/A and make that field blank
        for key in movie.keys():
            if movie[key] == "N/A":
                movie[key] = ""

        #make Ratings proper formatting
        # <source>:<value>;<source>:<value>
        tmp_r = []
        for rating in movie["Ratings"]:
            #join values with delimeter :
            tmp_r += [":".join(rating.values())]
        #join array with delimeter ;
        movie["Ratings"] = ";".join(tmp_r)

        #make IntegerField friendly
        movie["Runtime"] = int(movie["Runtime"].replace(" min", ""))
        movie["imdbVotes"] = int(movie["imdbVotes"].replace(",", ""))

        #make dates model friendly
        movie["Released"] = datetime.strptime(movie["Released"], "%d %b %Y").strftime("%Y-%m-%d")
        movie["DVD"] = datetime.strptime(movie["DVD"], "%d %b %Y").strftime("%Y-%m-%d")
        serializer = MovieSerializer(data=movie)
        if serializer.is_valid():
            serializer.save()
            resp = {"fetched_api_data": org_movie}
            resp.update(serializer.data)
            return JsonResponse(resp, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)

    if request.method == "GET":
        title = request.GET.get("title", "")
        year = request.GET.get("year", "")
        rated = request.GET.get("rated", "")
        runtime = request.GET.get("runtime", "")
        runtime_gte = request.GET.get("runtime_gte", "")
        #get all movies
        allmovies = Movie.objects.all()
        #filter if argument exists
        if not(title == ""):
            allmovies = allmovies.filter(Title__icontains=title)
        if not(year == ""):
            allmovies = allmovies.filter(Year=year)
        if not(rated == ""):
            allmovies = allmovies.filter(Rated__icontains=rated)
        if not(runtime == ""):
            allmovies = allmovies.filter(Runtime=runtime)
        if not(runtime_gte == ""):
            allmovies = allmovies.filter(Runtime__gte=runtime_gte)
        a = MovieSerializer(allmovies, many=True)
        return JsonResponse(a.data, safe=False, status=201)
