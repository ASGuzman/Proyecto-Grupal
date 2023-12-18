# Keys disponibles

<div align="center">Google Maps</div>

## Variables / Keys de negocios (metadata_sitios)
- Nombre
- Dirección
- id_mapa (Primary Key)
- Descripción
- Latitud
- Longitud
- Categoria (Tipo de Negocio)
- Score promedio
- Precio
- Horario
- Miscelanio
- Estado actual (Abierto o cerrado) + Hora
- url de busqueda
  
## Variables / Keys de reseñas (review-estados )
- ID usuario
- Nombre
- Hora (timespan)
- Score
- Reseña
- url de pics (fotos)
- id_mapa

<div align="center">Google Maps</div>

# Variables / Keys  del comercio (business.pkl)
- ID business
- Nombre negocio
- Direccion completa del negocio
- Ciudad
- Abreviacion del nombre de la ciudad
- Codigo postal
- Latitud
- Longitud
- Score promedio
- Numero de reseñas
- Estado (cerrado-0 / Abierto-1)
- Atributos del negocio
- Categoria negocio
- Horario
## Variables / Keys de reseñas (review.json)
- ID review
- ID usuario
- ID business
- Score
- Fecha reseña
- Reseña completa
- Votos reseñas util
- Votos reseña graciosa
- Votos reseña cool
## Variables / Keys de usuario (user.parquet)
- ID usuario
- Nombre usuario
- Numero de reseñas escritas
- Fecha de creacion del usuario en Yelp en formato YYYY-MM-DD
- Lista de amigos
- Número de votos marcados como útiles por el usuario
- Número de votos marcados como graciosos por el usuario
- Número de votos marcados como cool por el usuario
- Número de fans que tiene el usuario
- Años en los que el usuario fue miembro elite
- Promedio del valor de las reseñas
- Total de cumplidos 'hot' recibidos por el usuario
- Total de cumplidos varios recibidos por el usuario
- Total de cumplidos por el perfil recibidos por el usuario
- Total de cumplidos 'cute' recibidos por el usuario
- Total de listas de cumplidos recibidos por el usuario
- Total de cumplidos como notas recibidos por el usuario
- Total de cumplidos planos recibidos por el usuario
- Total de cumplidos 'cool' recibidos por el usuario
- Total de cumplidos graciosos recibidos por el usuario
- Número de complidos escritos recibidos por el usuario
- Número de cumplidos en foto recibidos por el usuario
  
## Variables / Keys de registros asociados al negocio (checkin.json )
- ID business
- Fechas de registro

## Variables / Keys de consejos o tips dados por el usuario (tip.json)
- Texto del tip
- Fecha de cuando se escribio
- Cumplidos totales
- ID business
- ID usuario
