# Generated by Django 2.1 on 2018-08-04 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_id', models.IntegerField()),
                ('comment_body', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=256)),
                ('Year', models.IntegerField()),
                ('Rated', models.CharField(blank=True, max_length=10)),
                ('Released', models.DateField(blank=True)),
                ('Runtime', models.IntegerField(blank=True)),
                ('Genre', models.CharField(blank=True, max_length=256)),
                ('Director', models.CharField(blank=True, max_length=128)),
                ('Writer', models.TextField(blank=True)),
                ('Actors', models.TextField(blank=True)),
                ('Plot', models.TextField(blank=True)),
                ('Language', models.CharField(blank=True, max_length=128)),
                ('Country', models.CharField(blank=True, max_length=64)),
                ('Awards', models.TextField(blank=True)),
                ('Poster', models.URLField(blank=True)),
                ('Ratings', models.TextField(blank=True)),
                ('Metascore', models.IntegerField(blank=True)),
                ('imdbRating', models.FloatField(blank=True)),
                ('imdbVotes', models.IntegerField(blank=True)),
                ('imdbID', models.CharField(blank=True, max_length=32)),
                ('Type', models.CharField(max_length=16)),
                ('DVD', models.DateField(blank=True)),
                ('BoxOffice', models.CharField(blank=True, max_length=32)),
                ('Production', models.CharField(max_length=64)),
                ('Website', models.URLField(blank=True)),
                ('Response', models.BooleanField()),
            ],
        ),
    ]
