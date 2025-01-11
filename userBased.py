import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Leer el archivo CSV sin encabezados
ratings_df = pd.read_csv("reviews.csv", names=["user_id", "movie_id", "rating"])

def user_based_recommendations(user_id, num_recommendations=4):
    # Crear matriz usuario-película
    user_movie_matrix = ratings_df.pivot_table(index="user_id", columns="movie_id", values="rating")

    # Llenar valores faltantes con 0
    user_movie_matrix = user_movie_matrix.fillna(0)

    # Calcular similitud de coseno entre usuarios
    user_similarity = cosine_similarity(user_movie_matrix)
    similarity_df = pd.DataFrame(user_similarity, index=user_movie_matrix.index, columns=user_movie_matrix.index)

    # Obtener usuarios similares al usuario actual
    similar_users = similarity_df[user_id].sort_values(ascending=False).drop(user_id)

    # Películas que el usuario actual no ha visto
    user_movies = set(user_movie_matrix.loc[user_id][user_movie_matrix.loc[user_id] > 0].index)
    recommendations = {}

    for similar_user in similar_users.index:
        similar_user_movies = set(user_movie_matrix.loc[similar_user][user_movie_matrix.loc[similar_user] > 0].index)
        for movie in similar_user_movies - user_movies:
            if movie not in recommendations:
                recommendations[movie] = user_movie_matrix.loc[similar_user, movie]

    # Ordenar recomendaciones por rating promedio y devolver las mejores
    sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)[:num_recommendations]
    return [movie_id for movie_id, _ in sorted_recommendations]