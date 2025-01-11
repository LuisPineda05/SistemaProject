import csv
import random

# Clase Review
class Review:
    def __init__(self, user, movie, rating):
        self.user = user
        self.movie = movie
        self.rating = rating

# Generar datos aleatorios para las reseñas
reviews = []
for _ in range(500):
    user_id = random.randint(0, 19)  # IDs de usuarios entre 0 y 19
    movie_id = random.randint(0, 1610)  # IDs de películas entre 0 y 1610
    rating = round(random.uniform(1.0, 5.0), 1)  # Calificación con un decimal entre 1.0 y 5.0
    reviews.append(Review(user=user_id, movie=movie_id, rating=rating))

# Guardar las reseñas en un archivo CSV
with open('reviews.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['user_id', 'movie_id', 'rating'])  # Encabezados
    for review in reviews:
        writer.writerow([review.user, review.movie, review.rating])

print("Archivo reviews.csv creado con éxito.")
