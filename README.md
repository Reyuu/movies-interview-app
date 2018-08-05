# Movies

REST API movie lookup tool written in python3 using Django and djangorestframework.

You can find hosted instance [here](http://movies.uguu.space/).

##Installation

Clone repository
`$ git clone https://github.com/Reyuu/movies-interview-app.git`

Setup virtualenv:
`$ virtualenv venv`

If your OS has Python 2.7 by default:
`$ virtualenv -p python3 venv`

Activate your venv:
`$ source venv/bin/activate`

Your prompt should change to something like this:
`(venv) $`
###Requirements
Requirements are contained in **requirements.txt** file.

Install:
`$ pip install -r requirements.txt`

###Configuration
This app operates by use of enviromental variables. So you either set them up in your platform or you set them inside **wsgi.py** file.

####Enviromental variables reference
------------
#####SECRET_KEY
Django secret key.

------------
#####OMDBAPI_KEY
Omdbapi.com api key.

------------
#####DJANGO_HOST
Host allowed, you should usually set this for your domain name.

------------
####wsgi.py setup
I recommend setting up your wsgi.py like below if you're going to host it using Apache soulution (how to [here](https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-ubuntu-16-04#configure-apache))

	import os
	import sys
	import site
	from django.core.wsgi import get_wsgi_application

	site.addsitedir("<path to venv>/lib/python3.5/site-packages")

	sys.path.append("<path to project root>/intapi")

	os.environ.setdefault("SECRET_KEY", "<your key>")
	os.environ.setdefault("OMDBAPI_KEY", "<your api key>")
	os.environ.setdefault("DJANGO_HOST", "<your domain>")
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intapi.settings')

	activate_env = os.path.expanduser("<path to venv>/bin/activate_this.py")
	exec(open(activate_env, "r").read(), dict(__file__=activate_env))

	#import django.core.handlers.wsgi
	#application = django.core.handlers.wsgi.WSGIHandler()

	application = get_wsgi_application()

####Database
Default backend is set to MySQL, although you're free to use anything. To change that edit **settings.py** according to Django documentation about [database backends](https://docs.djangoproject.com/en/2.0/ref/databases/ "database backends").

Default **.cnf** file for MySQL is set to **/etc/mysql/intapi.cnf**. You can change that in **settings.py**:

	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.mysql',
			'OPTIONS': {
				'read_default_file': '/etc/mysql/intapi.cnf',
			},
		}
	}

##Usage
###Frontend
I created simple frontend to test basic functionality of the nodes, should give you basic idea how to build on top of that.

###REST API

####POST
#####/movies
**Parametes**
`title` **required** movie title to fetch

**Response**
type: `application/json` full movie object and data fetched from API (available under `fetched_api_data` in json object)


------------
#####/comments
**Parametes**
`movie_id` **required** movie id to create comment to
`comment` **required** comment text

**Response**
type: `application/json` comment object

####GET
#####/movies
**Parametes**
`title` **optional** movie title filter
`year` **optional** year filter
`rated` **optional** rated filter
`runtime` **optional** runtime exact filter
`runtime_gte` **optional** runtime greater that and equal filter

**Response**
type: `application/json` fetch all movies (depends on applied filters)

------------
#####/comments
**Parametes**
`movie_id` **optional** filter comments bt movie id

**Response**
type: `application/json` fetch all comments (depends on applied filter)
