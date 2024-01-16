import streamlit as st
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import nltk

# Descargamos los recursos de NLTK 
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')

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

# Creamos la app de Streamlit
st.title("Recomendaciones de Restaurantes")

# Cargamos los datos en un dataframe
@st.cache_data
def cargar_datos():
    return pd.read_parquet("Sprint3/Modelo/modelo_df.parquet")

data = cargar_datos()

ciudad = st.selectbox("Seleccione el nombre de la ciudad:", data['city'].unique())
min_estrellas = st.slider("Seleccione la cantidad mínima de estrellas:", 0.0, 5.0, 0.0, 0.5)

# Función para obtener recomendaciones
@st.cache_data
def obtener_recomendaciones(data, nombre_ciudad, min_estrellas):
    data_ciudad = data[(data['city'] == nombre_ciudad) & (data['avg_rating'] >= min_estrellas)]

    if data_ciudad.empty:
        return "No hay restaurantes que cumplan con los criterios."
    
    # Aplicamos la función de análisis de sentimiento a la columna 'reseña'
    data_ciudad['polaridad'] = data_ciudad['text'].apply(obtener_polaridad)
    
    # Aplicamos la función de procesamiento de texto a la columna 'reseña_procesada'
    data_ciudad['reseña_procesada'] = data_ciudad['text'].apply(procesar_texto)

    # Creamos un vectorizador TF-IDF para procesar las reseñas
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_ciudad = tfidf_vectorizer.fit_transform(data_ciudad['reseña_procesada'])

    # Creamos el modelo de vecinos más cercanos (KNN) utilizando como metrica la similitud de coseno
    knn_model = NearestNeighbors(n_neighbors=5, metric='cosine')
    knn_model.fit(tfidf_ciudad)

    # Encontramos los vecinos más cercanos 
    _, indices = knn_model.kneighbors(tfidf_ciudad)

    # Obtenemos las recomendaciones de restaurantes
    top3_recomendaciones = data.iloc[indices[0]].head(3)['name'].tolist()

    # Verificamos si los primeros dos elementos son iguales y, en ese caso, seleccionar solo el primero
    if top3_recomendaciones[0] == top3_recomendaciones[1]:
        top3_recomendaciones = [top3_recomendaciones[0]] + top3_recomendaciones[2:]

    return top3_recomendaciones

if st.button("Obtener Recomendaciones"):
    recomendaciones = obtener_recomendaciones(data, ciudad, min_estrellas)
    st.success(f"Top 3 Recomendaciones para {ciudad}: {recomendaciones}")