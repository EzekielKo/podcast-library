from flask import Blueprint, render_template
from podcast.home import services
def create_home_blueprint(repo):
    home_blueprint = Blueprint('home_bp', __name__)
    @home_blueprint.route("/", methods=['GET'])
    def show_home():
        homepage_podcasts = services.get_homepage_podcasts(repo=repo)
        return render_template('/HomePage.html', podcasts=homepage_podcasts['podcasts'])
    return home_blueprint