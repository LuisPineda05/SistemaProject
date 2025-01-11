import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Leer el archivo CSV sin encabezado
df = pd.read_csv('reviews.csv', header=None)

# Asumimos que el archivo tiene 3 columnas: [user_id, movie_id, rating]
df.columns = ['user_id', 'movie_id', 'rating']

# Crear la matriz de calificaciones
ratings_matrix = df.pivot_table(index='user_id', columns='movie_id', values='rating').fillna(0)

# Calcular la similitud entre las películas (Item-based)
movie_similarity = cosine_similarity(ratings_matrix.T)

# Crear un DataFrame de similitud entre películas
movie_similarity_df = pd.DataFrame(movie_similarity, index=ratings_matrix.columns, columns=ratings_matrix.columns)

# Función para recomendar películas basadas en un movie_id
def recommend_movies(movie_id, num_recommendations=5):
    if movie_id not in movie_similarity_df.columns:
        print(f"Error: El movie_id {movie_id} no se encuentra en la matriz de similitudes.")
        return []

    # Obtener la similitud de la película
    similar_scores = movie_similarity_df[movie_id].sort_values(ascending=False)

    # Excluir la misma película
    similar_scores = similar_scores.drop(movie_id)

    # Obtener las 'num_recommendations' películas más similares
    recommended_movie_ids = similar_scores.head(num_recommendations).index.tolist()

    #print(f"Recomendaciones para la película {movie_id}: {recommended_movie_ids}")
    return recommended_movie_ids