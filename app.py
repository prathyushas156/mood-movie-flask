import os
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request, redirect, url_for
from models import db, Movie
import requests

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    DB_USER = os.getenv('DB_USER', 'mm_user')
    DB_PASS = os.getenv('DB_PASS', 'mm_pass')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_NAME = os.getenv('DB_NAME', 'mood_movies')
    TMDB_API_KEY = os.getenv('TMDB_API_KEY', '').strip()

    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    def fetch_poster_from_tmdb(title):
        """Search TMDb for a movie title and return a full poster URL or None."""
        if not TMDB_API_KEY or not title:
            return None
        try:
            params = {"api_key": TMDB_API_KEY, "query": title, "include_adult": "false"}
            resp = requests.get("https://api.themoviedb.org/3/search/movie", params=params, timeout=8)
            resp.raise_for_status()
            data = resp.json()
            results = data.get("results", [])
            if not results:
                return None
            top = results[0]
            poster_path = top.get("poster_path")
            if not poster_path:
                return None
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        except Exception as e:
            print("TMDb fetch error:", e)
            return None

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api/recommend', methods=['GET'])
    def recommend():
        mood = request.args.get('mood', '').strip().lower()
        if not mood:
            return jsonify({'error': 'No mood provided', 'results': []}), 400

        movies = Movie.query.filter(db.func.lower(Movie.mood) == mood).all()
        results = [{
            'id': m.id,
            'title': m.title,
            'genre': m.genre,
            'rating': float(m.rating) if m.rating is not None else None,
            'poster_url': m.poster_url
        } for m in movies]
        return jsonify({'mood': mood, 'results': results})

    # Dashboard
    @app.route('/dashboard')
    def dashboard():
        movies = Movie.query.order_by(Movie.created_at.desc()).all()
        return render_template('dashboard.html', movies=movies)

    @app.route('/dashboard/add', methods=['POST'])
    def add_movie():
        title = request.form.get('title')
        genre = request.form.get('genre')
        rating = request.form.get('rating') or None
        mood = request.form.get('mood', '').strip().lower()
        poster = request.form.get('poster_url') or None

        if not title or not mood:
            return redirect(url_for('dashboard'))

        if not poster:
            tmdb_poster = fetch_poster_from_tmdb(title)
            if tmdb_poster:
                poster = tmdb_poster

        m = Movie(title=title, genre=genre, rating=rating, mood=mood, poster_url=poster)
        db.session.add(m)
        db.session.commit()
        return redirect(url_for('dashboard'))

    @app.route('/dashboard/delete/<int:movie_id>', methods=['POST'])
    def delete_movie(movie_id):
        m = Movie.query.get(movie_id)
        if m:
            db.session.delete(m)
            db.session.commit()
        return redirect(url_for('dashboard'))

    # EDIT movie - show form
    @app.route('/dashboard/edit/<int:movie_id>', methods=['GET'])
    def edit_movie_form(movie_id):
        m = Movie.query.get(movie_id)
        if not m:
            return redirect(url_for('dashboard'))
        return render_template('edit.html', movie=m)

    # EDIT movie - submit updates
    @app.route('/dashboard/edit/<int:movie_id>', methods=['POST'])
    def edit_movie_submit(movie_id):
        m = Movie.query.get(movie_id)
        if not m:
            return redirect(url_for('dashboard'))

        m.title = request.form.get('title') or m.title
        m.genre = request.form.get('genre') or m.genre
        rating = request.form.get('rating')
        m.rating = float(rating) if rating else m.rating
        m.mood = request.form.get('mood', m.mood).strip().lower()
        poster = request.form.get('poster_url')
        if poster:
            m.poster_url = poster
        else:
            tmdb_poster = fetch_poster_from_tmdb(m.title)
            if tmdb_poster:
                m.poster_url = tmdb_poster

        db.session.commit()
        return redirect(url_for('dashboard'))

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
