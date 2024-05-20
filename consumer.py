from kafka import KafkaConsumer
import psycopg2
import json
import datetime

def insert_choice(data_to_insert):

    # extract the data to insert
    username = data_to_insert['username']
    created_timestamp = datetime.datetime.now()
    category = data_to_insert['category']
    gender = data_to_insert['gender']
    style = data_to_insert['style']
    size = data_to_insert['size']
    color = data_to_insert['color']

    print(created_timestamp)

    # Set the connection to the database
    conn = psycopg2.connect(
        host="localhost",
        database="clickstream",
        user="default",
        password="default123"
    )

    # Create a cursor to connect to the db
    cursor = conn.cursor()

    # Create the SQL query with the data to insert
    sql = f"INSERT INTO public.clickstream_data (username, creation_timestamp, category, gender, style, size, hex_color) VALUES ('{username}', '{created_timestamp}', '{category}', '{gender}', '{style}', '{size}', '{color}');"

    print(sql)

    # Execute the query
    cursor.execute(sql)

    # Commit the changes to bbdd
    conn.commit()

    # Close the connection and cursor
    cursor.close()
    conn.close()


# set the consumer config
consumer_config = {
    'bootstrap_servers': 'localhost:29092',  # Dirección del servidor de Kafka
    'group_id': 'my-consumer',  # ID del grupo de consumidores
    'auto_offset_reset': 'earliest'  # Configuración de inicio de lectura
}

# Create consumer
consumer = KafkaConsumer(**consumer_config)
# Subscribe to a specific topic
consumer.subscribe(topics=['clickstream'])

# Read messages from the topic
for message in consumer:
    data_to_insert = json.loads(message.value.decode('utf-8'))
    print(data_to_insert)
    insert_choice(data_to_insert)
