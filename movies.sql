-- create DB and user
CREATE DATABASE IF NOT EXISTS mood_movies;
CREATE USER IF NOT EXISTS 'mm_user'@'localhost' IDENTIFIED BY 'mm_pass';
GRANT ALL PRIVILEGES ON mood_movies.* TO 'mm_user'@'localhost';
FLUSH PRIVILEGES;

USE mood_movies;

CREATE TABLE IF NOT EXISTS movies (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  genre VARCHAR(100),
  rating DECIMAL(3,1),
  mood VARCHAR(50) NOT NULL,
  poster_url VARCHAR(500) NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- sample data
INSERT INTO movies (title, genre, rating, mood, poster_url) VALUES
('La La Land', 'Musical', 8.0, 'happy', NULL),
('Zootopia', 'Animation', 8.1, 'happy', NULL),
('The Fault in Our Stars', 'Romance', 7.7, 'sad', NULL),
('Before Sunrise', 'Romance', 8.1, 'romantic', NULL),
('The Pursuit of Happyness', 'Drama', 8.0, 'inspired', NULL),
('Ferris Bueller''s Day Off', 'Comedy', 7.8, 'bored', NULL);
