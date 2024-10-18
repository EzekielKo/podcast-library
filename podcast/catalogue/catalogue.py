from flask import Blueprint, render_template, request
from podcast.catalogue import services
import string

def create_catalogue_blueprint(repo):
    catalogue_blueprint = Blueprint('catalogue_bp', __name__)

    @catalogue_blueprint.route('/podcasts', methods=['GET'])
    def show_podcasts():
        current_letter = request.args.get('letter', 'A').upper()

        # Fetch all podcasts starting with the specified letter
        podcast_data = services.get_podcasts_by_letter(current_letter, repo=repo)

        return render_template(
            'catalogue.html',
            podcasts=podcast_data['podcasts'],
            current_letter=current_letter,
            letters=list(string.ascii_uppercase) + ['#']
        )

    return catalogue_blueprint
