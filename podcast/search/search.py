from flask import Blueprint, render_template, request
from podcast.adapters.repository import AbstractRepository
from podcast.search import services


def create_podcast_search_blueprint(repo: AbstractRepository):
    podcast_search_bp = Blueprint('podcast_search_bp', __name__)

    @podcast_search_bp.route('/search', methods=['GET'])
    def show_podcast_search():
        selected_category = request.args.get('selectCategory')
        search_input = request.args.get('search-input', '')
        current_page = request.args.get('page', 1, type=int)

        print(current_page)
        podcasts = []
        if search_input:
            if selected_category == 'Title':
                podcasts = services.get_podcasts_from_title(search_input, repo=repo)
            elif selected_category == 'Author':
                podcasts = services.get_podcasts_from_author(search_input, repo=repo)
            elif selected_category == 'Category':
                podcasts = services.get_podcasts_from_category(search_input, repo=repo)
            elif selected_category == 'Language':
                podcasts = services.get_podcasts_from_language(search_input, repo=repo)

        no_pages = (len(podcasts) + 9) // 10
        podcasts = services.get_page(current_page, podcasts)

        return render_template('podcastSearch.html',
                               selected_category=selected_category,
                               search_input=search_input,
                               podcasts=podcasts,
                               current_page=current_page,
                               number_of_pages=no_pages)

    return podcast_search_bp
