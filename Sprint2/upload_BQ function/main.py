from google.cloud import bigquery

project_name = 'my-project-89113-test'
datawarehouse = 'datawarehouse'

schemas_id = {
                'sitios_google':[
                bigquery.SchemaField("name", "STRING"),
                bigquery.SchemaField("address", "STRING"),
                bigquery.SchemaField("city", "STRING"),
                bigquery.SchemaField("state", "STRING"),
                bigquery.SchemaField("gmap_id", "STRING"),
                bigquery.SchemaField("latitude", "FLOAT64"),
                bigquery.SchemaField("longitude", "FLOAT64"),
                bigquery.SchemaField("category", "STRING"),
                bigquery.SchemaField("avg_rating", "FLOAT64"),
                bigquery.SchemaField("num_of_reviews", "INT64"),
                bigquery.SchemaField("price", "STRING"),
                bigquery.SchemaField("MISC", "STRING"),
                ],
                'reviews_google':[
                bigquery.SchemaField("user_id", "FLOAT64"),
                bigquery.SchemaField("rating", "INT64"),
                bigquery.SchemaField("text", "STRING"),
                bigquery.SchemaField("gmap_id", "STRING"),
                bigquery.SchemaField("date", "DATE"),
                bigquery.SchemaField("state", "STRING"),
                ],
                'business_yelp':[
                bigquery.SchemaField("business_id", "STRING"),
                bigquery.SchemaField("name", "STRING"),
                bigquery.SchemaField("city", "STRING"),
                bigquery.SchemaField("state", "STRING"),
                bigquery.SchemaField("latitude", "FLOAT64"),
                bigquery.SchemaField("longitude", "FLOAT64"),
                bigquery.SchemaField("stars", "FLOAT64"),
                bigquery.SchemaField("categories", "STRING"),
                ],
                'tips_yelp':[
                bigquery.SchemaField("user_id", "STRING"),
                bigquery.SchemaField("business_id", "STRING"),
                bigquery.SchemaField("text", "STRING"),
                bigquery.SchemaField("date", "INT64"),
                bigquery.SchemaField("compliment_count", "INT64"),
                ],
                'checkin_yelp':[
                bigquery.SchemaField("business_id", "STRING"),
                bigquery.SchemaField("date", "STRING"),
                ],
                'reviews_yelp':[
                bigquery.SchemaField("review_id", "STRING"),
                bigquery.SchemaField("user_id", "STRING"),
                bigquery.SchemaField("business_id", "STRING"),
                bigquery.SchemaField("stars", "INT64"),
                bigquery.SchemaField("useful", "INT64"),
                bigquery.SchemaField("funny", "INT64"),
                bigquery.SchemaField("cool", "INT64"),
                bigquery.SchemaField("text", "STRING"),
                bigquery.SchemaField("date", "DATE"),
                ],
                'users_yelp':[
                bigquery.SchemaField("user_id", "STRING"),
                bigquery.SchemaField("name", "STRING"),
                bigquery.SchemaField("review_count", "INT64"),
                bigquery.SchemaField("useful", "INT64"),
                bigquery.SchemaField("funny", "INT64"),
                bigquery.SchemaField("cool", "INT64"),
                bigquery.SchemaField("average_stars", "FLOAT64"),],
            }

def load_dw(event, context):
    file = event
    file_name=file['name']   
    table_name = file_name.split("/")[-1] 
    table_name = table_name.split(".")[0] # nombre del archivo sin el .parquet

    print(f"Se detectó que se subió el archivo {file_name} en el bucket {file['bucket']}.")
    source_bucket_name = file['bucket'] #Bucket donde esta el archivo
    
    if "Google/metadata_sitios" in file_name:
        table_name = 'sitios_google'
    elif "Google/reviews_estados" in file_name:
        table_name = 'reviews_google'
    elif "Yelp/business" in file_name:
        table_name = 'business_yelp'
    elif "Yelp/tips" in file_name:
        table_name='tips_yelp'
    elif "Yelp/checkin" in file_name:
        table_name='checkin_yelp'
    elif "Yelp/reviews" in file_name:
        table_name='reviews_yelp'
    elif "Yelp/users" in file_name:
        table_name='users_yelp'
    else:
        print(f"No se encontro la ruta en el file_name")

    # Constructor BigQuery client object.
    client = bigquery.Client()


    source_path = "gs://"+source_bucket_name+"/"+file_name # ruta al archivo 
    table_id = project_name + "." + datawarehouse + "." + table_name 
 
    print(f"Archivo source_bucket_name : {source_path}.")
    print(f"Archivo table_name : {table_name}.")
    print(f"Archivo table_id : {table_id}.")


    job_config = bigquery.LoadJobConfig(
        schema= schemas_id[table_name],
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        # The source format defaults to CSV, so the line below is optional.
        source_format=bigquery.SourceFormat.PARQUET,
    )
    #poner ubicación de archivo
    uri = source_path

    load_job = client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.

    destination_table = client.get_table(table_id)  # Make an API request.
    #Probando los rows cargados
    print("Loaded {} rows.".format(destination_table.num_rows))
