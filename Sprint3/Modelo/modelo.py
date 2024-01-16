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
blob.download_to_filename("Sprint3/Modelo/modelo_df_final2.parquet")

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
    data_ciudad = data[(data['city'] == nombre_ciudad) & (data['avg_rating'] >= min_estrellas)]

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
    knn_model = NearestNeighbors(n_neighbors=5, metric='cosine')
    knn_model.fit(tfidf_ciudad)

    # Encontramos los vecinos más cercanos 
    _, indices = knn_model.kneighbors(tfidf_ciudad)

    # Obtenemos las recomendaciones de restaurantes con nombre y dirección
    top3_recomendaciones = data_ciudad.iloc[indices[0]].head(3)[['name', 'address']]

    # Verificamos si los primeros dos elementos son iguales y, en ese caso, seleccionamos solo el primero
    if top3_recomendaciones.iloc[0]['name'] == top3_recomendaciones.iloc[1]['name']:
        top3_recomendaciones = top3_recomendaciones.iloc[1:]

    return top3_recomendaciones

# Función para obtener las coordenadas a partir de una dirección
def get_coordinates(address):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(address)
    if location:
        return [location.latitude, location.longitude]
    else:
        return None

# Cargamos los datos
data = pd.read_parquet("Sprint3/Modelo/modelo_df_final2.parquet")

# App de Streamlit
st.title("Recomendaciones de Restaurantes")
ciudad = st.selectbox("Seleccione el nombre de la ciudad:", data['city'].unique())
min_estrellas = st.slider("Seleccione la cantidad mínima de estrellas:", 0.0, 5.0, 0.0, 0.5)

if st.button("Obtener Recomendaciones"):
    recomendaciones = obtener_recomendaciones(data, ciudad, min_estrellas)
    st.markdown(f"## Top 3 Recomendaciones para {ciudad}")
    st.table(recomendaciones)

    # Creamos un mapa centrado en la primera dirección
    restaurant_map = folium.Map(location=get_coordinates(recomendaciones.iloc[0]['address']), zoom_start=15)

    # Agregamos marcadores para cada restaurante recomendado en el mapa
    for _, restaurante in recomendaciones.iterrows():
        coordinates = get_coordinates(restaurante['address'])
        if coordinates:
            # Personalizamos el ícono y el color del marcador
            icon = folium.Icon(color='blue', icon='cutlery', prefix='fa')  # Ícono de cubiertos azules
            folium.Marker(location=coordinates, popup=f"{restaurante['name']}: {restaurante['address']}", icon=icon).add_to(restaurant_map)

    # Guardamos el mapa como HTML para que Streamlit lo pueda leer
    restaurant_map.save("restaurant_map.html")

    # Mostramos el mapa en Streamlit mediante el componente HTML
    with open("restaurant_map.html", "r", encoding="utf-8") as file:
        map_html = file.read()
        st.components.v1.html(map_html, height=700)
