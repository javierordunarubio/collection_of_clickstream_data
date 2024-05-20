# Clickstream data app

In this repo we have built a toy app that simulates a real-time collection of "clickstream data" in an e-commerce webpage. We have written it in double quotes because what we store is the product selection of the users and not a detailed log of how participants navigate through the Web site during a task, which is what clickstream data is, but we will call it like that on the rest of the Readme file. We have used Docker to deploy a kafka cluster (with the zookeper services it needs for the infrastructure) with a kafka UI service. We also have deployed a postgres database with Docker to store all the data from the clickstream. The general idea is that we have built an streamlit app that tries to emulate an e-commerce webpage. There we have created some buying options to select the features of the products (it is a very simple webpage because the aim of the project is to collect the information from the webpage, not to build a complex webpage). In the end of the webpage, once we have selected the possible options, we have an "Add to chart" button. In order to collect this selection of the user in the database, we have created a Kafka producer (that connects to the local kafka cluster we have deployed with Docker), which, whenever this "Add to chart" is clicked, sends the information on an encoded json format to a concrete kafka topic. Then, we have another file that has a kafka consumer (which is subscribed to the topic the producer sends the information) listening, and, whenever a producer message arrives, it formats it propperly and inserts the data in the database.

## Prerequisites

* Having docker installed. If using WSL, check this guide: https://docs.docker.com/desktop/wsl/
* Having poetry (venv manager) installed. If you don't want to install it you can check the module tool.poetry.dependencies on the pyproject.toml file in the kafka_venv folder to check which are the necessary libraries and install them on the way you desire.

## Docker images used

The used images are defined in the file docker_images/docker-compose-zookeper-kafka-postgres.yml. As its known, Kafka often uses Zookeper for infrastructure (Zookeper is a distributed coordination and managing service that is used along with Kafka to ensure the integrity and the reliability of the kafka cluster). We have created 3 services of zookeper because it's reccomended to have an odd number of services of zookeper to prevent from failures (even if in our cluster we aren't going to receive lots of data). Apart from this zookeper we have deployed two kafka brokers and a kafka UI image to been able to see the state of the kafka cluster. To connect there, when everything is running propperly just search in the browser localhost:8080. Lastly, as we have commented before, we have deployed a postgres database service. In order to connect to the db and see the data more comfortably (using an UI) we have used the pgAdmin4 program (https://www.pgadmin.org/download/). In order to do that use the database, username and password defined in the compose file, as well as the localhost. To persist the data when the container is shut down we have mapped the data folder to inside the container.


## Steps to have everything running

1) Run the start_script.sh (execute ```bash start_script.sh```). This will deploy services defined in the file docker_images/docker-compose-zookeper-kafka-postgres.yml. Besides, it will activate the poetry venv. Once this is done, go back to the previous folder level (execute ```cd ..```).

2) Run the following SQL commands on the SQL database:

```
ALTER TABLE IF EXISTS public.clickstream_data
    OWNER to "default";
CREATE TABLE public.clickstream_data
(
    username character varying(32) NOT NULL,
    creation_timestamp timestamp(6) without time zone NOT NULL,
    category character varying(10),
    gender character varying(10),
    style character varying(20),
    size character varying(5),
    hex_color character varying(8),
    PRIMARY KEY (username, creation_timestamp)
);
```

You can do it directly using pgAdmin4 or accesing inside the container and executing from there the necessary commands. This can be done as it follows: 

* Access inside the running container: ```docker exec -it <your-postgres-container-id> bash```
* Run the following command to connect to the PostgreSQL console: ```psql -d clickstream -U default```
* Now you can run SQL commands directly. Execute the above query. 

3) Run the necessary python files:
* Open a terminal and run the command ```streamlit run streamlit_app.py```. This will launch the streamlit app. Whenever you select the options and click the "Add to chart" button, a kafka producer sends a message with that info to a concrete topic, as explained before.
* Open another terminal and run the command ```python3 consumer.py```. This file, as explained before, will run a kafka consumer that will remain listening to the topic the producer sends messages to. Whenever a message arrives it will extract the information from it and will format it and will insert it into the postgres database.
* Whenever you have completed the previous steps open the browser and search localhost:8501. You will see the toy e-commerce shop. We use that port because is the default streamlit port, but if desired it can be changed. Enter your username (if not provided the options are not displayed) and select the options you want (if desired you can leave them without selecting). When finished, click the "Add to chart button" to register this data on the db. If you want to modify configs on streamlit page (themes, runner, client...) just add the changes on the file ./streamlit/config.toml (https://docs.streamlit.io/develop/api-reference/configuration/config.toml).


4) The data will be stored in the database, so a further analysis could be processed there. As the scope of this project is not that one, we haven't done anything in that direction.