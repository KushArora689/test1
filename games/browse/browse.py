import games.adapters.repository as repo

from flask import render_template, Blueprint, request

from games.browse import services

browse_blueprint = Blueprint(
    'games_bp', __name__)


@browse_blueprint.route('/browse', methods=['GET'])
def browse_games():
    num_games = services.get_number_of_games(repo.repo_instance)
    all_games = services.get_games(repo.repo_instance)
    get_g2 = services.get_g(repo.repo_instance)
    page_no = int(request.args.get('page', 1))
    per_page = 10
    games = services.get_games_by_page(repo.repo_instance, page_no, per_page)
    return render_template(
        'browse.html',
        title=f'Browse Games | CS235 Game Library',
        heading='Browse Games',
        games=games,
        num_games=num_games,
        gz=get_g2,
        current_page=page_no,
        per_page=per_page
    )


@browse_blueprint.route('/browse/<genre>', methods=['GET'])
def browse_games_by_genre(genre):
    games_by_genre = services.get_games_by_genre(repo.repo_instance, genre)
    print(games_by_genre)
    return render_template(
        'genre_name.html',
        title=f'Browse {genre} Games | CS235 Game Library',
        heading=f'Browse {genre} Games',
        games=games_by_genre,
        selected_genre=genre
    )
