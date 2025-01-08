# En base a los links de Rotten Tomatoes, por medio de BeautifulSoup, encontramos las URL's de las imágenes y las guardamos en un nuevo csv
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests

data = pd.read_csv("peliculas.csv", delimiter=',')

# Crear una lista para almacenar las URLs de las imágenes con dimensiones modificadas
image_urls = []

# Iterar solo sobre los primeros 5 links en la columna del DataFrame
for link in data['link']:  # Seleccionar los primeros 5 elementos
    try:
        # Hacer la solicitud al link
        response = requests.get(link, timeout=10)
        response.raise_for_status()

        # Parsear el contenido de la página
        soup = BeautifulSoup(response.content, 'html.parser')

        # Buscar la imagen con alt que empieza con "Poster for"
        img_tag = soup.find('img', alt=lambda value: value and value.startswith('Poster for '))
        if img_tag and 'src' in img_tag.attrs:
            # Obtener la URL original de la imagen
            original_url = img_tag['src']

            # Modificar las dimensiones en la URL a 720x1080
            modified_url = original_url.replace('/68x102/', '/720x1080/')
            image_urls.append(modified_url)
        else:
            image_urls.append('No image found')

    except Exception as e:
        image_urls.append(f'Error: {e}')

# Imprimir las URLs de las imágenes con dimensiones 720x1080
print("URLs de las imágenes con dimensiones 720x1080:", image_urls)

import csv

with open("imágenes.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["image_url"])  # Escribe el encabezado
    for url in image_urls:
        writer.writerow([url])  # Escribe cada URL en una fila

print("Archivo imágenes.csv guardado con éxito.")