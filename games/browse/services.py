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
            'title': game.title,
            'game_url': game.genres,
        }
        game_dicts.append(game_dict)
    return game_dicts


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
