from games.adapters.repository import AbstractRepository
import games.adapters.repository as repo


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
