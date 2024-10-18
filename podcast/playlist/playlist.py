from flask import Blueprint, render_template, session, redirect, url_for, flash
from podcast.playlist import services
from podcast.authentication.authentication import login_required

def create_playlist_blueprint(repo):
    playlist_blueprint = Blueprint('playlist_bp', __name__)

    @playlist_blueprint.route('/playlist', methods=['GET'])
    @login_required
    def show_playlist():
        username = session.get('user_name')
        if not username:
            flash("You need to be logged in to view your playlists.", 'warning')
            return redirect(url_for('authentication_bp.login'))

        user = services.get_user_by_username(username, repo)
        if not user:
            flash("User not found.", 'error')
            return redirect(url_for('authentication_bp.login'))

        playlist = services.get_user_playlist(user, repo)
        return render_template('playlist.html', playlist=playlist)

    @playlist_blueprint.route('/remove/<int:episode_id>', methods=['POST'])
    @login_required
    def remove_from_playlist(episode_id):
        username = session.get('user_name')
        if not username:
            flash("You need to be logged in to modify your playlist.", 'warning')
            return redirect(url_for('authentication_bp.login'))

        user = services.get_user_by_username(username,repo)
        if not user:
            flash("User not found.", 'error')
            return redirect(url_for('authentication_bp.login'))

        success = services.remove_from_playlist(user, episode_id, repo)
        if success:
            flash("Episode removed from your playlist.", 'success')
        else:
            flash("Failed to remove episode. It may not be in your playlist.", 'error')

        return redirect(url_for('playlist_bp.show_playlist'))

    return playlist_blueprint
