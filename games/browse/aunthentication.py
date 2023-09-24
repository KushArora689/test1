import games.adapters.repository as repo

from flask import render_template, Blueprint, request

from games.browse import services

browse_blueprint = Blueprint(
    'games_bp', __name__)


@browse_blueprint.route('/register', methods=['GET'])
def register():
    num_games = services.get_number_of_games(repo.repo_instance)
    all_games = services.get_games(repo.repo_instance)
    gzz = services.get_g(repo.repo_instance)

    page_no = int(request.args.get('page', 1))
    per_page = 10
    games = services.get_games_by_page(repo.repo_instance, page_no, per_page)
    return render_template(
        'credentials.html',
        title=f'Browse Games | CS235 Game Library',
        heading='Browse Games',
        games=games,
        num_games=num_games,
        current_page=page_no,
        per_page=per_page,
        gzz = gzz
    )


