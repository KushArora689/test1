from bisect import insort_left
from typing import List
import os

from games import Game
from games.adapters.datareader.csvdatareader import GameFileCSVReader
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Genre, User, Review


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__games = list()
        self.__users = list()
        self.__reviews = list()
    def add_game(self, game: Game):
        if isinstance(game, Game):
            insort_left(self.__games, game)

    def get_games(self) -> List[Game]:
        return self.__games

    def get_number_of_games(self):
        return len(self.__games)

    def get_genres(self) -> List[Genre]:
        dir_name = os.path.dirname(os.path.abspath(__file__))
        games_file_name = os.path.join(dir_name, "data/games.csv")
        reader = GameFileCSVReader(games_file_name)
        reader.read_csv_file()

        genre = reader.dataset_of_genres
        return genre
    def get_games_by_page(self, page_no, per_page):
        start_index = (page_no - 1) * per_page
        end_index = start_index + per_page
        return self.__games[start_index: end_index]
    
    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self.__users if user.username == username), None)
    
    def add_review(self, review: Review):
        # call parent class first, add_comment relies on implementation of code common to all derived classes
        super().add_review(review)
        self.__reviews.append(review)

    def get_reviews(self):
        return self.__reviews

    def get_game(self, id: int) -> Game:
        game = None

        try:
            game = self.__articles_index[id]
        except KeyError:
            pass  # Ignore exception and return None.

        return article

def populate(repo: AbstractRepository):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    games_file_name = os.path.join(dir_name, "data/games.csv")
    reader = GameFileCSVReader(games_file_name)

    reader.read_csv_file()

    games = reader.dataset_of_games

    for game in games:
        repo.add_game(game)
