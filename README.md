<h2 align = center > 

![image](https://github.com/JorgeJola/Proyecto-Grupal/assets/113150003/b81e527a-c73c-4e82-aa8c-54688d9e7684)
 </h2>


Somos Data Seven Solution Consultant, una consultora ficticia especializada en análisis de datos. En el presente proyecto se lleva a cabo un análisis exhaustivo de las opiniones presentes en las plataformas de Google My Business y Yelp. El propósito de esta investigación es sumergirse en el vasto universo de opiniones proporcionadas por estos dos gigantes, con el fin de extraer conocimientos valiosos a través del análisis de sentimientos. Además, se persigue la creación de un sistema de recomendación que no solo comprenda la experiencia del usuario, sino que también tenga la capacidad de anticipar sus preferencias futuras.

Este análisis de datos nos capacita para ofrecer evaluaciones detalladas basadas en la información recopilada. Así, brindamos asesoría y recomendaciones a posibles inversores hipotéticos interesados en este proyecto, proporcionando información altamente valiosa para la toma de decisiones estratégicas. Además, nuestra labor contribuye a mejorar la imagen y reputación del negocio bajo consulta, fortaleciendo su posición en el mercado.

<h3 align = center> 

![image](https://github.com/JorgeJola/Proyecto-Grupal/assets/113150003/c5f48ee9-9c1d-4a82-8b85-79415c09b0d9) </h3>

<div id='id0' />

## Índice
1. [Propuesta de Trabajo](#id1)
2. [Data Engineering](#id2)
3. [Data Science & Analytics](#id3)
4. [Documentos Adicionales](#id4)
5. [Clona este repositorio](#id5)
6. [Autores](#id6)


<div id='id1' />

## Propuesta de Trabajo


Toda la documentación asociada a la Propuesta de Trabajo se encuentra en la Carpeta denominada [Sprint 1](Sprint1).

Allí encontrán un [pdf](Sprint1/Entregables_Sprint1.pdf) con  el alcance, objetivos, roles del equipo, metodología de trabajo y stack tecnologico a utilizar en el proyecto. También podrán encontrar un EDA preliminar para los datos de[Yelp](Sprint1/EDA_Yelp.ipynb) y [Google Maps](Sprint1/EDa_GoogleMaps.ipynb), y la [presentación](Sprint1/Presentacion_spring1.pdf) de la Demo 1.

   
### ¿Como lo hicimos Posible? 
  
1- Almacenamiento de datos crudos en el servicio en la nube Google Cloud Storage

2- Extracción y transformación de datos con python usando Cloud Functions.

3- Análisis de datos en la nube con BigQuery

4- Modelos de Machine Learning con las librerias de Scikit-learn, Keras y TensorFlow, deployados con la libreria Streamlit

5- Visualización y reportes con Google Data Looker conectado desde BigQuery



![image](https://github.com/JorgeJola/Proyecto-Grupal/assets/113150003/f2c76ade-e9e2-4cc6-ae85-b58158e49750)

  
[volver al índice](#id0)


  
<div id='id2' />  

 
## Data Engineering   
Toda la documentación asociada al Data Engineering se encuentra en la Carpeta denominada [Sprint 2](Sprint2).
  

[volver al índice](#id0)
   
<div id='id3' />  

 
## Data Science & Analytics
  ### Sistema de Recomendación de Restaurantes 

Se presenta una aplicación interactiva diseñada para descubrir recomendaciones de restaurantes, integrando técnicas avanzadas como análisis de sentimientos y vecinos más cercanos. Construida con Streamlit, la aplicación proporciona una interfaz amigable que simplifica la exploración de opciones culinarias en una ciudad específica.

### Funcionalidades Clave

1. **Análisis de Sentimientos:**
   - El código realiza un análisis de sentimientos en las reseñas de restaurantes, evaluando su positividad.

2. **Procesamiento de Texto:**
   - Se aplican técnicas de procesamiento de texto, como tokenización y lematización, para comprender mejor el contenido de las reseñas.

3. **Recomendaciones Personalizadas:**
   - Mediante técnicas de aprendizaje automático, como TF-IDF y vecinos más cercanos (KNN), se generan sugerencias de restaurantes basadas en las preferencias del usuario.

4. **Interfaz de Usuario Interactiva:**
   - Streamlit proporciona una interfaz fácil de usar que permite al usuario seleccionar la ciudad de interés y ajustar el umbral mínimo de estrellas para las recomendaciones.

5. **Visualización Visual:**
   - Las recomendaciones se presentan de manera clara en una tabla clasificada y en un mapa interactivo con marcadores para cada restaurante sugerido.

### Uso

1. **Instalación de Dependencias:**
   - Asegúrate de tener instaladas todas las dependencias necesarias ejecutando `pip install -r requirements.txt`.

2. **Ejecución de la Aplicación:**
   - Inicia la aplicación ejecutando `streamlit run modelo.py`.

3. **Exploración de Recomendaciones:**
   - Selecciona la ciudad de tu elección y ajusta el umbral de estrellas. Haz clic en "Obtener Recomendaciones" para descubrir sugerencias de restaurantes.

4. **Acceso a la Aplicación en Línea:**
   - [Explora recomendaciones de restaurantes aquí](https://modelo-restaurantes.onrender.com) para disfrutar de una experiencia gastronómica personalizada.

¡Disfruta explorando y descubriendo nuevas delicias culinarias con nuestro sistema interactivo de recomendación de restaurantes!

[volver al índice](#id0)

    
<div id='id4' />

 
## Documentos Adicionales
* [Diccionario de datos]()
  
[volver al índice](#id0)
  

<div id='id5' />    

 
## Clona este repositorio 👍
Explora nuestro proyecto clonandolo en tu computadora 

```bash
git clone https://github.com/JorgeJola/Proyecto-Grupal.git
```
  
[volver al índice](#id0)  
    

  
<div id='id6' />  
 
## Autores   
Aylén Sol Guzman, Data Scientist - [@ASGuzman](https://github.com/ASGuzman)  
Maria Marcela Diaz, Data Analyst - [@]()  
Priscila Muñiz, Data Analyst - [@priscilamuniz](https://github.com/priscilamuniz)   
Jorge Andres Jola Hernandez, Data Engineer  - [@JorgeJola](https://github.com/JorgeJola)  
Franco Dylan Damian Luna Pedroso, Data Engineer - [@]() 

[volver al índice](#id0)
