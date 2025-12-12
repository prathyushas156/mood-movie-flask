from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(100))
    rating = db.Column(db.Numeric(3,1))
    mood = db.Column(db.String(50), nullable=False)
    poster_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
