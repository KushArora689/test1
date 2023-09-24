from games.adapters.repository import AbstractRepository
import games.adapters.repository as repo
from werkzeug.security import generate_password_hash, check_password_hash
from games.domainmodel.model import User

class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass

def get_number_of_games(repo: AbstractRepository):
    return repo.get_number_of_games()


def get_games(repo: AbstractRepository):
    games = repo.get_games()
    game_dicts = []
    for game in games:
        game_dict = {
            'game_id': game.game_id,
            'release_date': game.release_date,
            'price': game.price,
            'publisher': game.publisher,
            'title': game.title,
            'description': game.description,
            'image_url': game.image_url
        }
        game_dicts.append(game_dict)
    return sorted(game_dicts, key=lambda x: x["title"])


def get_g(repo: AbstractRepository):
    g = repo.get_genres()
    genre2 = [genre.genre_name for genre in g]

    return genre2


def get_games_by_genre(repo: AbstractRepository, genre):
    games_by_genre = []

    for game in repo.get_games():
        for i in game.genres:
            if i.genre_name == genre:
                games_by_genre.append(game)
            break

    return games_by_genre

def get_games_by_page(repo: AbstractRepository, page_no, per_page):
    all_games = repo.get_games()
    start_index = (page_no - 1) * per_page
    end_index = start_index + per_page
    return all_games[start_index:end_index]

def add_user(username: str, password: str, repo: AbstractRepository):
    # Check that the given user name is available.
    user = repo.get_user(username)
    if user is not None:
        raise NameNotUniqueException

    # Encrypt password so that the database doesn't store passwords 'in the clear'.
    password_hash = generate_password_hash(password)

    # Create and store the new User, with password encrypted.
    user = User(username, password_hash)
    repo.add_user(user)


def get_user(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    return user_to_dict(user)


def authenticate_user(username: str, password: str, repo: AbstractRepository):
    authenticated = False

    user = repo.get_user(username)
    if user is not None:
        authenticated = check_password_hash(user.password, password)
    if not authenticated:
        raise AuthenticationException

def get_game(game_id: int, repo: AbstractRepository):
    game = repo.get_article(article_id)

    if article is None:
        raise NonExistentArticleException

    return article_to_dict(article)


# ===================================================
# Functions to convert model entities to dictionaries
# ===================================================

def user_to_dict(user: User):
    user_dict = {
        'username': user.username,
        'password': user.password
    }
    return user_dict