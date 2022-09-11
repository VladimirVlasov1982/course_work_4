from project.config import config
from project.models import Genre, Director, Movie, User, FavouriteMovie
from project.server import create_app, db

app = create_app(config)


@app.shell_context_processor
def shell():
    return {
        "db": db,
        "Genre": Genre,
        "Director": Director,
        "Movie": Movie,
        "User": User,
        "FavouriteMovie": FavouriteMovie,
    }


if __name__ == "__main__":
    app.run()
