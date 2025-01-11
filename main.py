import csv
import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk
import urllib.request
import io
import project
import ssl
from collections import defaultdict
import numpy as np
import coseno
from tkinter import PhotoImage


class MovieApp:
    def __init__(self, root, movies_list):
        self.root = root
        self.movies_list = movies_list
        self.root.title("CineScope")

        # Fijar el tamaño de la ventana
        self.root.geometry("1080x720")
        self.root.resizable(False, False)  # No permitir el cambio de tamaño

        # Título en la parte superior (CineScope)
        self.title_label = tk.Label(root, text="CineScope", font=("Helvetica", 36), anchor="center")
        self.title_label.pack(pady=20)

        # Barra de búsqueda con el botón de Lupita, más grande
        self.search_frame = tk.Frame(root)
        self.search_frame.pack(pady=10)

        self.search_entry = tk.Entry(self.search_frame, font=("Helvetica", 18), width=50)  # Más grande y más ancho
        self.search_entry.grid(row=0, column=0, padx=10)

        self.search_button = tk.Button(self.search_frame, text="🔍", font=("Helvetica", 18), command=self.search)
        self.search_button.grid(row=0, column=1)

        # Canvas y scrollbar
        self.canvas = tk.Canvas(root)
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollable_frame = tk.Frame(self.canvas)

        # Crear el lienzo con un contenedor desplazable
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.display_movies()

    def display_movies(self):
        row = 0
        column = 0
        for movie in self.movies_list[0:10]:
            movie_frame = tk.Frame(self.scrollable_frame)
            movie_frame.grid(row=row, column=column, padx=10, pady=5, sticky="w")

            # Frame para la imagen y los datos
            movie_inner_frame = tk.Frame(movie_frame)
            movie_inner_frame.grid(row=0, column=0, sticky="w")

            # Cargar y redimensionar la imagen
            try:
                with urllib.request.urlopen(movie.get_image_url()) as url:
                    img_data = url.read()
                    image = Image.open(io.BytesIO(img_data))
                    image = image.resize((100, 150), Image.Resampling.LANCZOS)
                    image = ImageTk.PhotoImage(image)

                image_label = tk.Label(movie_inner_frame, image=image)
                image_label.image = image  # Mantener la referencia de la imagen
                image_label.grid(row=0, column=0, padx=10)
            except Exception as e:
                print(f"Error al cargar la imagen: {e}")
                image_label = tk.Label(movie_inner_frame, text="No image", width=20, height=10)
                image_label.grid(row=0, column=0, padx=10)

            # Mostrar los datos
            movie_info = f"{movie.get_title()} ({movie.year})\n{movie.genre}\nCritic Score: {movie.critic_score}\nPeople Score: {movie.people_score}"
            data_label = tk.Label(movie_inner_frame, text=movie_info, justify="left")
            data_label.grid(row=0, column=1, padx=10)

            # Botón para ver detalles
            details_button = tk.Button(movie_inner_frame, text="Ver detalles", command=lambda m=movie: self.show_movie_details(m))
            details_button.grid(row=1, column=1, pady=5)

            column += 1
            if column == 2:  # Ajustar para la siguiente fila
                column = 0
                row += 1

        self.scrollable_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def show_movie_details(self, movie):
        # Crear una nueva ventana
        details_window = tk.Toplevel(self.root)
        details_window.title(movie.title)
        details_window.geometry("720x900")  # Altura aumentada

        # Mostrar el título (arriba, grande y centrado)
        title_label = tk.Label(details_window, text=movie.title, font=("Helvetica", 24, "bold"), wraplength=700,
                               anchor="center")
        title_label.pack(pady=10)

        # Mostrar la imagen (centrada debajo del título)
        try:
            with urllib.request.urlopen(movie.get_image_url()) as url:
                img_data = url.read()
                image = Image.open(io.BytesIO(img_data))
                image = image.resize((200, 300), Image.Resampling.LANCZOS)
                image = ImageTk.PhotoImage(image)

            image_label = tk.Label(details_window, image=image)
            image_label.image = image
            image_label.pack(pady=10)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            image_label = tk.Label(details_window, text="No image available", width=20, height=10)
            image_label.pack(pady=10)

        # Mostrar detalles adicionales (debajo de la imagen)
        details_frame = tk.Frame(details_window)
        details_frame.pack(pady=10)

        # Mostrar cada detalle con etiquetas en negrita y valores normales
        details = [
            ("Género:", movie.get_genre()),
            ("Año:", movie.get_year()),
            ("Puntuación crítica:", movie.get_critic_score()),
            ("Puntuación del público:", movie.get_people_score()),
        ]

        for label, value in details:
            row_frame = tk.Frame(details_frame)
            row_frame.pack(anchor="w", pady=2)
            bold_label = tk.Label(row_frame, text=label, font=("Helvetica", 12, "bold"))
            bold_label.pack(side="left")
            value_label = tk.Label(row_frame, text=value, font=("Helvetica", 12))
            value_label.pack(side="left")

        # Mostrar la sinopsis (con márgenes laterales)
        synopsis_frame = tk.Frame(details_window, padx=20)  # Márgenes laterales
        synopsis_frame.pack(fill="x", pady=10)
        synopsis_label = tk.Label(
            synopsis_frame,
            text=f"Sinopsis:\n{movie.get_synopsis()}",
            font=("Helvetica", 12),
            wraplength=680,  # Ajuste al ancho interno con márgenes
            justify="left",
        )
        synopsis_label.pack()

        # Obtener las películas más similares
        similar_movies = coseno.recommend_movies(movie.get_id(), 4)

        # Input para puntuar
        rate_frame = tk.Frame(details_window)
        rate_frame.pack(pady=10)

        rate_label = tk.Label(rate_frame, text="Ingresa tu puntuación (1-5):", font=("Helvetica", 12))
        rate_label.pack(side="left", padx=5)

        rate_entry = tk.Entry(rate_frame, font=("Helvetica", 12), width=5)
        rate_entry.pack(side="left", padx=5)

        # Crear un frame para las películas recomendadas
        recommended_frame = tk.Frame(details_window)
        recommended_frame.pack(pady=10)

        # Crear el label para "Películas Similares" con mayor tamaño y alineado a la izquierda
        similar_movies_label = tk.Label(recommended_frame, text="Películas Similares", font=("Helvetica", 16, "bold"))
        similar_movies_label.grid(row=0, column=0, columnspan=1, pady=10, sticky="w",
                                  padx=(10, 0))  # Agregar margen a la izquierda

        # Iterar para mostrar las películas similares debajo del primer label
        for i, movie_index in enumerate(similar_movies):
            # Cargar la imagen de la película
            with urllib.request.urlopen(self.movies_list[movie_index].get_image_url()) as url:
                img_data = url.read()
                image = Image.open(io.BytesIO(img_data))
                image = image.resize((100, 150), Image.Resampling.LANCZOS)  # Redimensionar la imagen
                image = ImageTk.PhotoImage(image)

            # Crear una columna para la imagen y el nombre
            movie_column = tk.Frame(recommended_frame)
            movie_column.grid(row=1, column=i, padx=10, pady=5,  sticky="w"
                             )  # Asegurarse de que las imágenes estén alineadas a la izquierda

            # Mostrar la imagen de la película
            image_label = tk.Label(movie_column, image=image)
            image_label.image = image  # Mantener una referencia a la imagen
            image_label.pack()

            # Mostrar el nombre de la película debajo de la imagen
            name_label = tk.Label(movie_column, text=self.movies_list[movie_index].get_title(), font=("Helvetica", 10))
            name_label.pack()

        # Crear el label para "Películas que Creemos que te Gustarán" con mayor tamaño y alineado a la izquierda
        recommended_movies_label = tk.Label(recommended_frame, text="Películas que Creemos que te Gustarán",
                                            font=("Helvetica", 16, "bold"))
        recommended_movies_label.grid(row=2, column=0, columnspan=1, pady=10, sticky="w",
                                      padx=(10, 0))  # Agregar margen a la izquierda



        # Añadir un botón de cierre
        close_button = tk.Button(details_window, text="Cerrar", command=details_window.destroy)
        close_button.pack(pady=10)

        def submit_rating(movie, rate_entry):
            try:
                rating = float(rate_entry.get())
                if 1.0 <= rating <= 5.0:
                    with open("reviews.csv", mode="a", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow([0, movie.get_id(), rating])  # ID de usuario 0 y ID de película

                    messagebox.showinfo("Puntuar", "¡Puntuación registrada exitosamente!")
                else:
                    messagebox.showerror("Error", "Por favor, ingresa un número entre 1 y 5.")
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingresa un número válido.")

        # Al hacer clic en el botón, pasamos el argumento correcto con lambda
        rate_button = tk.Button(
            rate_frame,
            text="Puntuar",
            font=("Helvetica", 12),
            command=lambda: submit_rating(movie, rate_entry)  # Pasamos movie y rate_entry
        )
        rate_button.pack(side="left", padx=5)

    def search(self):
        search_term = self.search_entry.get()
        search_results = project.searchFilm(search_term.lower())
        self.movies_list = search_results
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.display_movies()

if __name__ == "__main__":
    ssl._create_default_https_context = ssl._create_unverified_context
    root = tk.Tk()
    app = MovieApp(root, project.movies_list)
    root.mainloop()