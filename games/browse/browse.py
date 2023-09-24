import games.adapters.repository as repo
from flask_wtf import FlaskForm
from flask import Blueprint, render_template, redirect, url_for, session, request
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError
from better_profanity import profanity
from password_validator import PasswordValidator

from functools import wraps
from games.browse import services

browse_blueprint = Blueprint(
    'games_bp', __name__)


@browse_blueprint.route('/browse', methods=['GET'])
def browse_games():
    num_games = services.get_number_of_games(repo.repo_instance)
    all_games = services.get_games(repo.repo_instance)
    gzz = services.get_g(repo.repo_instance)

    page_no = int(request.args.get('page', 1))
    per_page = 10
    games = services.get_games_by_page(repo.repo_instance, page_no, per_page)
    return render_template(
        'browse.html',
        title=f'Browse Games | CS235 Game Library',
        heading='Browse Games',
        games=games,
        num_games=num_games,
        current_page=page_no,
        per_page=per_page,
        gzz = gzz
    )


@browse_blueprint.route('/browse/<genre>', methods=['GET'])
def browse_games_by_genre(genre):
    games_by_genre = services.get_games_by_genre(repo.repo_instance, genre)
    get_g2 = services.get_g(repo.repo_instance)
    
    return render_template(
        'genre_name.html',
        title=f'Browse {genre} Games | CS235 Game Library',
        heading=f'Browse {genre} Games',
        games=games_by_genre,
        selected_genre=genre,
        gzz = get_g2
    )

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('games_bp.login'))
        return view(**kwargs)
    return wrapped_view

@browse_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    username_not_unique = None
    get_g2 = services.get_g(repo.repo_instance)
    if form.validate_on_submit():
        # Successful POST, i.e. the user name and password have passed validation checking.
        # Use the service layer to attempt to add the new user.
        try:
            services.add_user(form.username.data, form.password.data, repo.repo_instance)

            # All is well, redirect the user to the login page.
            return redirect(url_for('games_bp.login'))
        except services.NameNotUniqueException:
            username_not_unique = 'Your user name is already taken - please supply another'

    # For a GET or a failed POST request, return the Registration Web page.
    return render_template(
        'credentials.html',
        title='Register',
        form=form,
        username_error_message=username_not_unique,
        handler_url=url_for('games_bp.register'),
        gzz = get_g2
        
    )


@browse_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    username_not_recognised = None
    password_does_not_match_username = None
    get_g2 = services.get_g(repo.repo_instance)
    if form.validate_on_submit():
        # Successful POST, i.e. the user name and password have passed validation checking.
        # Use the service layer to lookup the user.
        try:
            user = services.get_user(form.username.data, repo.repo_instance)

            # Authenticate user.
            services.authenticate_user(user['username'], form.password.data, repo.repo_instance)

            # Initialise session and redirect the user to the home page.
            session.clear()
            session['username'] = user['username']
            print(session['username'])
            return redirect(url_for('games_bp.browse_games'))

        except services.UnknownUserException:
            # User name not known to the system, set a suitable error message.
            username_not_recognised = 'User name not recognised - please supply another'

        except services.AuthenticationException:
            # Authentication failed, set a suitable error message.
            password_does_not_match_username = 'Password does not match supplied user name - please check and try again'

    # For a GET or a failed POST, return the Login Web page.
    return render_template(
        'credentials.html',
        title='Login',
        username_error_message=username_not_recognised,
        password_error_message=password_does_not_match_username,
        form=form,
        gzz = get_g2
        
    )
class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = u'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'
        self.message = message

    def __call__(self, form, field):
        print("PasswordValid validator called with field:", field.name)
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        print(self.message)
        
        if not schema.validate(field.data):
            print("Validation failed for field:", field.name)
            raise ValidationError(self.message)
        
class RegistrationForm(FlaskForm):
    username = StringField('Username', [
        DataRequired(message='Your user name is required'),
        Length(min=3, message='Your user name is too short')])
    password = PasswordField('Password', [
        DataRequired(message='Your password is required'),
        PasswordValid()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', [
        DataRequired()])
    password = PasswordField('Password', [
        DataRequired()])
    submit = SubmitField('Login')


@browse_blueprint.route('/reviews', methods=['GET', 'POST'])
@login_required
def comment_on_article():
    # Obtain the user name of the currently logged in user.
    username = session['username']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an article id, when subsequently called with a HTTP POST request, the article id remains in the
    # form.
    form = CommentForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the comment text has passed data validation.
        # Extract the article id, representing the commented article, from the form.
        game_id = int(form.game_id.data)

        # Use the service layer to store the new comment.
        services.add_comment(game_id, form.comment.data, username, repo.repo_instance)

        # Retrieve the article in dict form.
        article = services.get_article(game_id, repo.repo_instance)

        # Cause the web browser to display the page of all articles that have the same date as the commented article,
        # and display all comments, including the new comment.
        return redirect(url_for('news_bp.articles_by_date', date=article['date'], view_comments_for=game_id))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the article id, representing the article to comment, from a query parameter of the GET request.
        game_id = int(request.args.get('article'))

        # Store the article id in the form.
        form.game_id.data = game_id
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the article id of the article being commented from the form.
        game_id = int(form.game_id.data)

    # For a GET or an unsuccessful POST, retrieve the article to comment in dict form, and return a Web page that allows
    # the user to enter a comment. The generated Web page includes a form object.
    article = services.get_article(game_id, repo.repo_instance)
    return render_template(
        'comment_on_game.html',
        title='Edit article',
        article=article,
        form=form,
        handler_url=url_for('news_bp.comment_on_article'),
        
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', [
        DataRequired(),
        Length(min=4, message='Your comment is too short'),
        ProfanityFree(message='Your comment must not contain profanity')])
    game_id = HiddenField("Article id")
    submit = SubmitField('Submit')