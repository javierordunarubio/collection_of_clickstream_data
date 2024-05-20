import streamlit as st
import time
from kafka import KafkaProducer
import json

# set the producer config
producer_config = {"bootstrap_servers": "localhost:29092", "client_id": "my-producer"}

# Create productor
producer = KafkaProducer(**producer_config)

# define the topic to which we will send messages
topic = 'clickstream'


def search_with_progress():
    # Create a progress bar initially hidden
    progress_bar = st.progress(0)

    # Simulate a search
    with st.spinner("Searching..."):
        for i in range(101):
            # Update the progress bar value
            progress_bar.progress(i)
            time.sleep(0.01)

    # Show a success message when the search is complete
    st.success("Search completed")

def display_add_to_chart_option_and_send_producer(username, category, gender, selected_option, size, color):
    # CSS to inject contained in a string
    css = """
    <style>
    div.stButton > button:first-child {
        background-color: #FF8B8B;
        color: black;
    }
    </style>
    """

    # Inject CSS with Markdown
    st.markdown(css, unsafe_allow_html=True)

    # create a button to add the product to the cart
    if st.button("Add to cart"):
        # assign the product to the category    
        if category == "Shirts :shirt:":
            product = "shirt"
        elif category == "Trousers :jeans:":
            product = "trousers"

        if gender == 'Man :boy:':
            gender_to_show = 'man'
        else:
            gender_to_show = 'woman'
        data_to_send = {'username': username, 'category': product, 'gender':gender_to_show, 'style': selected_option, 'size': size, 'color': color}
        st.write(data_to_send)
        # send message using kafka producer. first we need to convert the data to json format and encode it
        message = json.dumps(data_to_send).encode('utf-8')
        producer.send(topic, value=message)
        producer.flush() # Flush the producer buffer
        st.success("The product has been added to the cart.")



def main():
    # Set the page configuration options
    st.set_page_config(
        layout="centered",
        page_title="Clickstream analysis with Kafka and Streamlit",
        page_icon=":repeat:",
        initial_sidebar_state="expanded",
    )

    # create a title
    st.title("Clickstream analysis with Kafka and Streamlit")

    # add a description
    st.write(
        "This is a simple example of how to use Kafka and Streamlit to analyze clickstream data. Let's simulate we are an e-commerce web and start by entering the username."
    )

    # creater an entering for the user
    username = st.text_input("Enter your username", placeholder="username_example", value=None)

    if username is not None:

        # create a button
        category = st.radio(
            "Category to look at:", ["Shirts :shirt:", "Trousers :jeans:"], index=None
        )

        if category == "Shirts :shirt:":
            st.write("You selected shirts.")
            search_with_progress()

            # select gender
            gender = st.radio(
                "Select if the shirt is for man or for woman:",
                ["Man :boy:", "Woman :girl:"],
                index=None,
            )

            # shirt style selection
            options = [
                "Plain t-shirt",
                "Pocket t-shirt",
                "Polo shirt",
                "Button-shirt",
                "Hawaiian shirt",
            ]

            # create a list of images associated to each style
            links_to_images = [
                "https://www.thefashionisto.com/wp-content/uploads/2023/07/Types-of-Shirts-Men-White-T-Shirt.jpg",
                "https://www.thefashionisto.com/wp-content/uploads/2023/07/Types-of-Shirts-Men-Pocket-T-Shirt-UNIQLO-Orange.jpg",
                "https://www.thefashionisto.com/wp-content/uploads/2023/07/Types-of-Shirts-Men-Polo-Shirt-Abercrombie-Fitch.jpg",
                "https://www.thefashionisto.com/wp-content/uploads/2023/07/Types-of-Shirts-Men-Button-down.jpg",
                "https://www.thefashionisto.com/wp-content/uploads/2023/07/Types-of-Shirts-Men-Hawaiian-INC.jpg",
            ]

            # radiobutton to select the style
            selected_option = st.radio("Select the style of shirt:", options, index=None)

            # Obtain the desired index if an option is selected
            if selected_option is not None:
                index_option = options.index(selected_option)

                # Mostramos la imagen correspondiente a la opción seleccionada
                st.image(links_to_images[index_option], caption=selected_option, width=200)

            # select the color
            color = st.color_picker("Pick A Color", "#000000")

            # select size
            size = st.selectbox("Select size", ["S", "M", "L", "XL"], index=None)

            # display option
            display_add_to_chart_option_and_send_producer(username, category, gender, selected_option, size, color)

        elif category == "Trousers :jeans:":
            st.write("You selected trousers.")
            search_with_progress()

            # select gender
            gender = st.radio(
                "Select if the shirt is for man or for woman:",
                ["Man :boy:", "Woman :girl:"],
                index=None
            )
            # shirt style selection
            options = [
                "Chinos",
                "Pleated pants",
                "Joggers",
                "Cargo pants",
                "Cropped pants",
            ]

            # create a list of images associated to each style
            links_to_images = [
                "https://cdn.shopify.com/s/files/1/0526/5496/4893/files/chinos_1024x1024.jpg?v=1693377246",
                "https://cdn.shopify.com/s/files/1/0526/5496/4893/files/pleated-pants_1024x1024.jpg?v=1693377360",
                "https://cdn.shopify.com/s/files/1/0526/5496/4893/files/joggers_1024x1024.jpg?v=1693377382",
                "https://cdn.shopify.com/s/files/1/0526/5496/4893/files/caro-pants_1024x1024.jpg?v=1693377405",
                "https://cdn.shopify.com/s/files/1/0526/5496/4893/files/cropped-pants_1024x1024.jpg?v=1693377858",
            ]

            # radiobutton to select the style
            selected_option = st.radio("Select the style of shirt:", options, index=None)

            # Obtain the desired index if an option is selected
            if selected_option is not None:
                index_option = options.index(selected_option)

                # Mostramos la imagen correspondiente a la opción seleccionada
                st.image(links_to_images[index_option], caption=selected_option, width=200)
            
            # select the color
            color = st.color_picker("Pick A Color", "#000000")

            # select size
            size = st.selectbox("Select size", ["S", "M", "L", "XL"], index=None)


            # display option
            display_add_to_chart_option_and_send_producer(username, category, gender, selected_option, size, color)

            





main()
