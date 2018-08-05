from django.test import TestCase, RequestFactory, Client
from .views import movie, comment
from .models import Movie, Comment
import json
import requests

# Create your tests here.

class MovieAndCommentTest(TestCase):
    def setUp(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        self.movie = Movie(id=0, Title="Gone with the Wind", Year=1992, Type="movie", Response="True")
        self.comment = Comment(movie_id=0, comment_body="Some comment very nice")
        self.movie.save()
        self.comment.save()

    def test_movie_post(self):
        title = "Guardians of the Galaxy"
        response = self.client.post("/movies", {"title": title})
        self.assertEqual(response.status_code, 201)
        j = json.loads(response.content)
        self.assertEqual(j["Title"], title)

    def test_movie_get(self):
        response = self.client.get("/movies")
        self.assertEqual(response.status_code, 201)
        j = json.loads(response.content)
        self.assertEqual(len(j), Movie.objects.count())
    
    def test_movie_get_title(self):
        title = "Gone with the Wind"
        response = self.client.get("/movies", {"title": title})
        self.assertEqual(response.status_code, 201)
        j = json.loads(response.content)
        self.assertEqual(j[0]["Title"], title)

    def test_comment_post(self):
        data = {"movie_id": 0, "comment": "Very nice!"}
        response = self.client.post("/comments", data)
        self.assertEqual(response.status_code, 201)
        j = json.loads(response.content)
        self.assertEqual(j["movie_id"], data["movie_id"])
        self.assertEqual(j["comment_body"], data["comment"])

    def test_comment_get(self):
        response = self.client.get("/comments")
        self.assertEqual(response.status_code, 201)
        j = json.loads(response.content)
        self.assertEqual(len(j), Comment.objects.count())
    
    def test_comment_get_by_movie_id(self):
        data = {"movie_id": 0}
        response = self.client.get("/comments", )
        self.assertEqual(response.status_code, 201)
        j = json.loads(response.content)
        self.assertEqual(len(j), Comment.objects.filter(movie_id=data["movie_id"]).count())