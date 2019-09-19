# MovieBase
MovieBase prove REST API which allows to get list of movies from database, 
add new movies, add comments to movies, get lists of movies and also the rank
of movies based on numbers of comment for specific time period.

## Run app
To run the application you need docker and that's all.

Just download repository, go to the main folder where docker-compose.yml file
is located and run:
```bash
$ docker-compose up --build
``` 

Now you can reach app at port `8080`.

## Heroku
This app is also hosted on *Heroku* so if you don't want to download repository,
you can just go to https://moviebase-igakar.herokuapp.com/. 

### How to use it?
With MovieBase API you can list existing movies, comments and also add new ones. 

#### List movies and comments
- To list all movies got to:

    https://moviebase-igakar.herokuapp.com/movies/

- To list all comments got to:

    https://moviebase-igakar.herokuapp.com/comments/

- To get the movie rank you must specify `date_from` and `date_to` parameters 
in format `YYYY-MM-DD (year-month-day)` like:

    https://moviebase-igakar.herokuapp.com/top/?date_from=1990-1-10&date_to=1990-9-28
    
#### Add movies and comments
To add movies you must send `POST` http request to  https://moviebase-igakar.herokuapp.com/movies/
with `'title'` parameters. Then it is checked if this title already exists in database, 
in case is not it will be added. The data about movies are download from [OMDb API](http://omdbapi.com/).

To create comment you must sent `POST` http request to  https://moviebase-igakar.herokuapp.com/comments/
with `'movie_id'` and `'body'` parameters which refer accordingly to **movie id**
of existing movie and content of comment.
