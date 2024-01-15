import streamlit as st
import pandas as pd
from google.cloud import storage
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.neighbors import NearestNeighbors

# Cargar datos desde Google Cloud Storage
bucket_name = "pf_cleaned_data"
blob_name = "Modelo_df/maps_concatenado2.parquet"

storage_client = storage.Client()
bucket = storage_client.get_bucket(bucket_name)
blob = bucket.blob(blob_name)

# Descargar el conjunto de datos localmente
blob.download_to_filename("Sprint3/Modelo/modelo_df.parquet")

# Realizar análisis de sentimiento usando NLTK
sia = SentimentIntensityAnalyzer()

# Función para obtener polaridad
def obtener_polaridad(reseña):
    sentiment_score = sia.polarity_scores(reseña)
    return sentiment_score['compound']

# Leer datos
data = pd.read_parquet("Sprint3/Modelo/modelo_df.parquet")

# Aplicar análisis de sentimiento
data['polaridad'] = data['text'].apply(obtener_polaridad)

# Tokenización y lematización
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Función para procesar texto
def procesar_texto(texto):
    tokens = word_tokenize(texto.lower())
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalpha() and token not in stop_words]
    return ' '.join(tokens)

# Procesar texto
data['reseña_procesada'] = data['text'].apply(procesar_texto)

# Streamlit App
st.title("Recomendaciones de Restaurantes")

ciudad = st.selectbox("Seleccione el nombre de la ciudad:", data['city'].unique())
min_estrellas = st.slider("Seleccione la cantidad mínima de estrellas:", 0.0, 5.0, 0.0, 0.5)

# Función para obtener recomendaciones
def obtener_recomendaciones(nombre_ciudad, min_estrellas):
    # Crear un vectorizador TF-IDF para procesar las reseñas
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_ciudad = tfidf_vectorizer.fit_transform(data_ciudad['reseña_procesada'])

    # Encontrar vecinos más cercanos basados en similitud de coseno
    _, indices = knn_model.kneighbors(tfidf_ciudad)

    # Obtener recomendaciones de restaurantes
    top3_recomendaciones = data.iloc[indices[0]].head(3)['name'].tolist()

    return top3_recomendaciones

if st.button("Obtener Recomendaciones"):
    recomendaciones = obtener_recomendaciones(ciudad, min_estrellas)
    st.success(f"Top 3 Recomendaciones para {ciudad}: {recomendaciones}")
