import streamlit as st
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import nltk
import folium
from geopy.geocoders import Nominatim
from google.cloud import storage
import json
import os

# Descargamos los recursos de NLTK 
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


# Cargamos datos desde Google Cloud Storage
bucket_name = "pf_cleaned_data"
blob_name = "Modelo_df/maps_concatenado3.parquet"

storage_client = storage.Client()
bucket = storage_client.get_bucket(bucket_name)
blob = bucket.blob(blob_name)

# Descargamos el conjunto de datos localmente
# Cargamos datos desde Google Cloud Storage (si aún no está cargado)
parquet_file_path = "Sprint3/Modelo/modelo_df_final_bucket.parquet"
if not os.path.exists(parquet_file_path):
    blob.download_to_filename(parquet_file_path)
blob.download_to_filename("Sprint3/Modelo/modelo_df_final_bucket.parquet")

# Realizamos el análisis de sentimiento usando NLTK
sia = SentimentIntensityAnalyzer()

# Creamos una funcion para obtener la polaridad del analisis de sentimiento de las reviews
def obtener_polaridad(reseña):
    sentiment_score = sia.polarity_scores(reseña)
    return sentiment_score['compound']

# Creamos una funcion para procesar el texto, donde se hace tokenizacion y lematizacion
def procesar_texto(texto):
    tokens = word_tokenize(texto.lower())
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalpha() and token not in stop_words]
    return ' '.join(tokens)

# Función para obtener recomendaciones
@st.cache_data
def obtener_recomendaciones(data, nombre_ciudad, min_estrellas):
    data_ciudad = data[(data['city'] == nombre_ciudad) & (data['Estrellas'] >= min_estrellas)]

    if data_ciudad.empty:
        return "No hay restaurantes que cumplan con los criterios."
    
    # Aplicamos la función de análisis de sentimiento a la columna 'text'
    data_ciudad['polaridad'] = data_ciudad['text'].apply(obtener_polaridad)
    
    # Aplicamos la función de procesamiento de texto a la columna 'text'
    data_ciudad['reseña_procesada'] = data_ciudad['text'].apply(procesar_texto)

    # Creamos un vectorizador TF-IDF para procesar las reseñas
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_ciudad = tfidf_vectorizer.fit_transform(data_ciudad['reseña_procesada'])

    # Creamos el modelo de vecinos más cercanos (KNN) utilizando como métrica la similitud de coseno
    knn_model = NearestNeighbors(n_neighbors=10, metric='cosine')
    knn_model.fit(tfidf_ciudad)

    # Encontramos los vecinos más cercanos 
    _, indices = knn_model.kneighbors(tfidf_ciudad)

    # Asegúrate de que indices[0] tenga al menos 3 elementos
    top3_recomendaciones = data_ciudad.iloc[indices[0]].head(10)[['Name', 'Address', 'latitude', 'longitude', 'Estrellas']]
    top3_recomendaciones = top3_recomendaciones.drop_duplicates(subset='Name').head(3)

    return top3_recomendaciones

# Función para obtener las coordenadas a partir de las columnas latitude y longitude
def get_coordinates_from_columns(df):
    if len(df) == 1:
        return df[['latitude', 'longitude']].values.flatten().tolist()
    else:
        return df[['latitude', 'longitude']].values.tolist()

# Cargamos los datos
data = pd.read_parquet("Sprint3/Modelo/modelo_df_final_bucket.parquet").sample(n=10000, random_state=42)

# App de Streamlit
st.title("Recomendaciones de Restaurantes")
ciudad = st.selectbox("Seleccione el nombre de la ciudad:", data['city'].unique())
min_estrellas = st.slider("Seleccione la cantidad mínima de estrellas:", 3.5, 5.0, 3.5, 0.1)

if st.button("Obtener Recomendaciones"):
    recomendaciones = obtener_recomendaciones(data, ciudad, min_estrellas)
    st.markdown(f"## Recomendaciones para {ciudad}")
    # Mostrar solo las columnas 'name', 'address' y 'Estrellas' en la tabla
    columns_to_display = ['Name', 'Address','Estrellas']
    st.table(recomendaciones[columns_to_display].round({'Estrellas': 1}).reset_index(drop=True))
    
    # Creamos un mapa centrado en la primera dirección
    restaurant_map = folium.Map(location=get_coordinates_from_columns(recomendaciones.iloc[[0]]), zoom_start=15)

    # Agregamos marcadores para cada restaurante recomendado en el mapa
    for _, restaurante in recomendaciones.iterrows():
        coordinates = get_coordinates_from_columns(restaurante)
        if coordinates:
            # Personalizamos el ícono y el color del marcador
            icon = folium.Icon(color='blue', icon='cutlery', prefix='fa') 
            folium.Marker(location=coordinates, popup=f"{restaurante['Name']}: {restaurante['Address']}", icon=icon).add_to(restaurant_map)

    # Guardamos el mapa como HTML para que Streamlit lo pueda leer
    restaurant_map.save("restaurant_map.html")

    # Mostramos el mapa en Streamlit mediante el componente HTML
    with open("restaurant_map.html", "r", encoding="utf-8") as file:
        map_html = file.read()
        st.components.v1.html(map_html,height=700)