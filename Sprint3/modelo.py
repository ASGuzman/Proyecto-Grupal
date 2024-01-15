import streamlit as st
import pandas as pd
from google.cloud import storage
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos desde Google Cloud Storage
bucket_name = "pf_cleaned_data"
blob_name = "Modelo_df/maps_concatenado2.parquet"

storage_client = storage.Client()
bucket = storage_client.get_bucket(bucket_name)
blob = bucket.blob(blob_name)

# Descargar el conjunto de datos localmente
blob.download_to_filename("modelo_df.parquet")

# Realizar análisis de sentimiento usando NLTK
sia = SentimentIntensityAnalyzer()

# Función para obtener polaridad
def obtener_polaridad(reseña):
    sentiment_score = sia.polarity_scores(reseña)
    return sentiment_score['compound']

# Leer datos
data = pd.read_parquet("modelo_df.parquet")

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

# Crear un vectorizador TF-IDF para procesar las reseñas
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(data['reseña_procesada'])

# Calcular similitud de coseno entre las reseñas
cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Crear un modelo de vecinos más cercanos (KNN)
knn_model = NearestNeighbors(n_neighbors=5, metric='cosine')
knn_model.fit(tfidf_matrix)

# Función para obtener recomendaciones
def obtener_recomendaciones(nombre_ciudad, min_estrellas):
    # Filtrar por ciudad y por cantidad mínima de estrellas
    data_ciudad = data[(data['city'] == nombre_ciudad) & (data['avg_rating'] >= min_estrellas)]

    if data_ciudad.empty:
        return "No hay restaurantes que cumplan con los criterios."

    # Calcular TF-IDF para las reseñas de la ciudad filtrada
    tfidf_ciudad = tfidf_vectorizer.transform(data_ciudad['reseña_procesada'])

    # Encontrar vecinos más cercanos basados en similitud de coseno
    _, indices = knn_model.kneighbors(tfidf_ciudad)

    # Obtener recomendaciones de restaurantes
    top3_recomendaciones = data.iloc[indices[0]].head(3)['name'].tolist()

    return top3_recomendaciones

# Streamlit App
st.title("Recomendaciones de Restaurantes")


# Visualización de datos
st.subheader("Distribución de Ratings")
fig, ax = plt.subplots()
sns.histplot(data['avg_rating'], bins=10, kde=True, ax=ax)
st.pyplot(fig)

ciudad = st.selectbox("Seleccione el nombre de la ciudad:", data['city'].unique())
min_estrellas = st.slider("Seleccione la cantidad mínima de estrellas:", 0.0, 5.0, 0.0, 0.5)

if st.button("Obtener Recomendaciones"):
    recomendaciones = obtener_recomendaciones(ciudad, min_estrellas)
    st.success(f"Top 3 Recomendaciones para {ciudad}: {recomendaciones}")

# Añade más elementos según tus preferencias
st.markdown("## Sobre nosotros")
st.info("Somos un equipo dedicado a proporcionar las mejores recomendaciones de restaurantes.")

# Agrega enlaces o información adicional
st.markdown("[Visítanos en nuestro sitio web](https://www.tusitio.com)")

# Personaliza el pie de página
st.markdown("© 2024 Tu Empresa. Todos los derechos reservados.")
