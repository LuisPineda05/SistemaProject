import csv

import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests

data = pd.read_csv("peliculas.csv", delimiter=',')

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.reviews = []

    def add_review(self, review):
        self.reviews.append(review)

    def __str__(self):
        return f"User(username={self.username}, email={self.email}, reviews={len(self.reviews)})"


class Movie:
    def __init__(self, title, year, synopsis, critic_score, people_score, consensus, total_reviews, total_ratings,
                 genre, director, producer, writer, release_date, box_office, runtime, production_company, crew, image_url):
        self.title = title
        self.year = year
        self.synopsis = synopsis
        self.critic_score = critic_score
        self.people_score = people_score
        self.consensus = consensus
        self.total_reviews = total_reviews
        self.total_ratings = total_ratings
        self.genre = genre
        self.director = director
        self.producer = producer
        self.writer = writer
        self.release_date = release_date
        self.box_office = box_office
        self.runtime = runtime
        self.production_company = production_company
        self.crew = crew


        self.reviews = []

        self.imageUrl = image_url

    def set_image_url(self, url):
        self.imageUrl = url

    def get_image_url(self):
        return self.imageUrl

    def add_review(self, review):
        self.reviews.append(review)

    def average_rating(self):
        if not self.reviews:
            return None
        return sum(review.rating for review in self.reviews) / len(self.reviews)

    def get_title(self):
        return self.title

    def get_synopsis(self):
        return self.synopsis

    def get_genre(self):
        return self.genre


    def get_director(self):
        return self.director

    def get_producer(self):
        return self.producer

    def get_writer(self):
        return self.writer

    def get_release_date(self):
        return self.release_date

    def get_box_office(self):
        return self.box_office

    def get_runtime(self):
        return self.runtime

    def get_production_company(self):
        return self.production_company

    def get_crew(self):
        return self.crew



    def __str__(self):
        return f"Movie(title={self.title}, year={self.year}, genre={self.genre}, director={self.director}, imageUrl={self.imageUrl})"


class Review:
    def __init__(self, user, movie, rating, comment):
        self.user = user
        self.movie = movie
        self.rating = rating
        self.comment = comment

        # Agregar la reseña a las listas de usuario y película
        user.add_review(self)
        movie.add_review(self)

    def __str__(self):
        return f"Review(user={self.user.username}, movie={self.movie.title}, rating={self.rating}, comment={self.comment})"



# crear movies
image_urls = []
# Abrir el archivo CSV y leerlo
with open("imágenes.csv", newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)  # Usamos DictReader para acceder por el nombre de las columnas
    for row in reader:
        # Asumimos que la columna de enlaces se llama 'link', cámbiala si es necesario
        image_urls.append(row['image_url'])

i = 0

# Inicializa la lista para almacenar las películas
movies_list = []

# Itera sobre cada fila del DataFrame
for _, row in data.iterrows():
    # Verifica si ya existe una película con el mismo título
    if not any(movie.title == row['title'] for movie in movies_list):
        # Crea un objeto Movie con los valores de la fila
        movie = Movie(
            title=row['title'],
            year=row['year'],
            synopsis="No synopsis available" if row['synopsis'] == "" or pd.isna(row['synopsis']) else row['synopsis'],
            critic_score=row['critic_score'],
            people_score=row['people_score'],
            consensus=row['consensus'],
            total_reviews=row['total_reviews'],
            total_ratings=row['total_ratings'],
            genre="No genre available" if row['genre'] == "" or pd.isna(row['genre']) else row['genre'],
            director="No director available" if row['director'] == "" or pd.isna(row['director']) else row['director'],
            producer=row['producer'],
            writer=row['writer'],
            release_date=row['release_date_(theaters)'],
            box_office=row['box_office_(gross_usa)'],
            runtime=row['runtime'],
            production_company=row['production_co'],
            crew="No crew available" if row['crew'] == "" or pd.isna(row['crew']) else row['crew'],
            image_url=image_urls[i]
        )
        # Agrega el objeto Movie a la lista
        movies_list.append(movie)
    i = i + 1  # Incrementa el índice para la URL de la imagen


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Obtener todas las sinopsis
synopsis_list = [movie.get_synopsis().lower() + " " + movie.get_title().lower() + " " + movie.get_genre().lower() + " " + movie.get_crew().lower() + " " + movie.get_director().lower() for movie in movies_list]

# Crear el vectorizador TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')

# Ajustar el modelo y transformar las sinopsis en una matriz TF-IDF
tfidf_matrix = vectorizer.fit_transform(synopsis_list)

# Función para recomendar películas basado en la similitud coseno
def recommend_movies(query, tfidf_matrix, movies_list, top_n = 5):
    # Transformar la consulta de búsqueda en un vector TF-IDF
    query_tfidf = vectorizer.transform([query])

    # Calcular la similitud coseno entre la consulta y todas las sinopsis
    similarity_scores = cosine_similarity(query_tfidf, tfidf_matrix).flatten()

    # Obtener los índices de las películas más similares
    top_indices = similarity_scores.argsort()[-top_n:][::-1]

    # Mostrar las películas recomendadas
    print(f"Recomendaciones para la consulta: '{query}':\n")
    results = []
    for i in top_indices:
        print(f"- {movies_list[i].get_title()} (Similitud: {similarity_scores[i]:.4f})")
        if similarity_scores[i] > 0:
            results.append(movies_list[i])
    return results

# Ejemplo de consulta de búsqueda
def searchFilm(text, n=10):
    return recommend_movies(text, tfidf_matrix, movies_list, n)