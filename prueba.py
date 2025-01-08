import ssl
import urllib.request
import io
from PIL import Image, ImageTk
import tkinter as tk

# Crear un contexto SSL que no verifique el certificado
ssl._create_default_https_context = ssl._create_unverified_context

class WebImage:
    def __init__(self, url):
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data))  # Abrir la imagen desde los datos binarios
        self.image = ImageTk.PhotoImage(image)

    def get(self):
        return self.image

# Configuración de la ventana principal de Tkinter
root = tk.Tk()
root.title("Weather")

# URL de la imagen que quieres cargar
link = "https://openweathermap.org/themes/openweathermap/assets/img/logo_white_cropped.png"

# Cargar la imagen usando la clase WebImage
img = WebImage(link).get()

# Crear un label para mostrar la imagen
imagelab = tk.Label(root, image=img)
imagelab.grid(row=0, column=0)

# Iniciar el loop de Tkinter
root.mainloop()
