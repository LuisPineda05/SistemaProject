import tkinter as tk
from PIL import Image, ImageTk
import urllib.request
import io
import project
import ssl

from project import movies_list


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
        for movie in self.movies_list:
            movie_frame = tk.Frame(self.scrollable_frame)
            movie_frame.grid(row=row, column=column, padx=10, pady=5, sticky="w")

            # Frame para la imagen y los datos
            movie_inner_frame = tk.Frame(movie_frame)
            movie_inner_frame.grid(row=0, column=0, sticky="w")

            # Cargar y redimensionar la imagen
            try:
                # Descargar la imagen desde la URL
                with urllib.request.urlopen(movie.get_image_url()) as url:
                    img_data = url.read()
                    image = Image.open(io.BytesIO(img_data))

                    # Redimensionar la imagen a un tamaño más pequeño
                    image = image.resize((100, 150), Image.Resampling.LANCZOS)
                    image = ImageTk.PhotoImage(image)

                image_label = tk.Label(movie_inner_frame, image=image)
                image_label.image = image  # Mantener la referencia de la imagen
                image_label.grid(row=0, column=0, padx=10)

            except Exception as e:
                print(f"Error al cargar la imagen: {e}")
                image_label = tk.Label(movie_inner_frame, text="No image", width=20, height=10)
                image_label.grid(row=0, column=0, padx=10)

            # Mostrar los datos a la derecha de la imagen
            movie_info = f"{movie.title} ({movie.year})\n{movie.genre}\nCritic Score: {movie.critic_score}\nPeople Score: {movie.people_score}"
            data_label = tk.Label(movie_inner_frame, text=movie_info, justify="left")
            data_label.grid(row=0, column=1, padx=10)

            # Ajustar la fila y columna para la siguiente película
            column += 1
            if column == 2:  # Cuando llegue a la segunda columna, pasar a la siguiente fila
                column = 0
                row += 1

        self.scrollable_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def search(self):
        # Obtener el término de búsqueda
        search_term = self.search_entry.get()

        # Llamar a la función searchFilm de project para obtener los resultados
        search_results = project.searchFilm(search_term.lower())

        # Actualizar la lista de películas con los resultados de la búsqueda
        self.movies_list = search_results

        # Limpiar el contenedor de películas antes de insertar los nuevos resultados
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Volver a mostrar las películas con los nuevos resultados
        self.display_movies()


if __name__ == "__main__":
    # Crear un contexto SSL que no verifique el certificado
    ssl._create_default_https_context = ssl._create_unverified_context
    root = tk.Tk()
    app = MovieApp(root, project.movies_list[0:10])  # Mostrar las primeras 10 películas

    root.mainloop()
