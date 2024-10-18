from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from podcast.adapters.repository import AbstractRepository
from podcast.description import services
from podcast.authentication.authentication import login_required

from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange
def create_podcast_description_blueprint(repo: AbstractRepository):
    podcast_description_bp = Blueprint('podcast_description_bp', __name__)

    @podcast_description_bp.route('/description/<int:podcast_id>')
    def show_podcast_description(podcast_id):
        rendered_by_catalogue = request.args.get('rendered_by_catalogue', 'False').lower() == 'true'
        podcast_data = services.get_podcast_data(podcast_id, repo)
        nav_ids = services.get_previous_and_next_podcast_ids(podcast_id, repo)

        podcast = repo.get_podcast(podcast_id)


        user_name = session.get('user_name', None)
        user_playlist = False
        if user_name:
            user_playlist = services.get_user_playlist(services.get_user_by_username(user_name, repo), repo)

        return render_template(
            'podcastDescription.html',
            podcast=podcast_data,
            previous_id=nav_ids['previous_id'],
            next_id=nav_ids['next_id'],
            rendered_by_catalogue=rendered_by_catalogue,
            playlist=user_playlist
        )


    @podcast_description_bp.route('/review', methods=['GET', 'POST'])
    @login_required
    def review_on_podcast():
        # Obtain the username of the currently logged in user.
        user_name = session['user_name']

        # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
        # the form with an article id, when subsequently called with a HTTP POST request, the article id remains in the
        # form.
        form = ReviewForm()

        if form.validate_on_submit():
            print("Form submitted successfully")
            print(f"Rating: {form.rating.data}, Comment: {form.comment.data}, Podcast ID: {form.podcast_id.data}")
            # Successful POST, i.e. the comment text has passed data validation.
            # Extract the podcast id, representing the commented article, from the form.
            podcast_id = int(form.podcast_id.data)

            podcast = services.get_podcast(podcast_id, repo)
            user = services.get_user_by_username(user_name, repo)
            # Use the service layer to store the new comment.
            print(user)
            services.add_review_to_podcast(user,form.rating.data, form.comment.data, podcast, repo)

            # Retrieve the podcast in dict form.
            podcast_data = services.get_podcast_data(podcast_id, repo)
            reviews = podcast.reviews


            # Cause the web browser to display the page of all articles that have the same date as the commented article,
            # and display all comments, including the new comment.
            return redirect(url_for('podcast_description_bp.show_podcast_description', podcast_id=podcast.id))

        if request.method == 'GET':
            # Request is a HTTP GET to display the form.
            # Extract the article id, representing the article to comment, from a query parameter of the GET request.
            podcast_id = int(request.args.get('podcast'))

            # Store the article id in the form.
            form.podcast_id.data = podcast_id
        else:
            # Request is a HTTP POST where form validation has failed.
            # Extract the article id of the article being commented from the form.
            podcast_id = int(form.podcast_id.data)

        # For a GET or an unsuccessful POST, retrieve the article to comment in dict form, and return a Web page that allows
        # the user to enter a comment. The generated Web page includes a form object.
        podcast_data = services.get_podcast_data(podcast_id, repo)
        return render_template(
            'addReview.html',
            title='Add Review',
            podcast=podcast_data,
            form=form,
            handler_url=url_for('podcast_description_bp.review_on_podcast'),
        )

    @podcast_description_bp.route('/add_to_playlist/<int:podcast_id>/<int:episode_id>', methods=['POST'])
    @login_required
    def add_to_playlist(podcast_id, episode_id):
        rendered_by_catalogue = request.form.get('rendered_by_catalogue', 'False').lower() == 'true'

        username = session['user_name']
        user = services.get_user_by_username(username, repo)
        if user is None:
            flash('User not found.', 'error')
            return redirect(url_for('authentication_bp.login'))

        episode = services.get_episode(episode_id, repo)
        if episode is None:
            flash('Episode not found.', 'error')
            return redirect(url_for('podcast_description_bp.show_podcast_description', podcast_id=podcast_id))

        playlist = services.get_user_playlist(user, repo)
        if not playlist:
            playlist = services.create_playlist(user, f"{username}'s playlist", repo)

        message = services.add_episode_to_playlist(playlist, episode, repo)
        if message:
            flash(f"{episode.title} added to your playlist.")

        # Pass `rendered_by_catalogue` in the redirect URL
        return redirect(url_for('podcast_description_bp.show_podcast_description', podcast_id=podcast_id,
                                rendered_by_catalogue=rendered_by_catalogue))

    return podcast_description_bp


class ReviewForm(FlaskForm):
    # Comment input field
    comment = TextAreaField('Comment', [
        DataRequired(),
        Length(min=1, max=50, message='Your comment is too short')
    ])

    # Rating input field (1-5 stars), which will be rendered as radio buttons
    rating = IntegerField('Rating (out of 5)', [
        DataRequired(),
        NumberRange(min=1, max=5, message='Rating must be between 1 and 5')
    ])

    # Hidden field for the podcast
    podcast_id = HiddenField("Article id")

    # Submit button
    submit = SubmitField('Submit Review')
