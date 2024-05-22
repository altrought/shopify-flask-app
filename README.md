# Shopify Flask Application

## Setup and Run

1. Clone the repository:
   ```bash
   git clone <repository-link>
   cd shopify-flask-app
   
2. Create and activate a virtual environment:
   ```bash 
    python3 -m venv venv
    source venv/bin/activate

3. Install the dependencies:

    ```bash

    pip install -r requirements.txt

4. Create a config.py file with the following content:
    ```bash
    SHOPIFY_STORE_URL = "Provided in the challenge"
    SHOPIFY_API_VERSION = "2024-01"
    SHOPIFY_ACCESS_TOKEN = "Provided in the challenge"

5. Run the Flask application:

    ```bash
    python app.py

6. Access the application by navigating to http://127.0.0.1:5000 in your web browser.


## Assumptions and Design Decisions

### Order Availability Assumption

During the development of the application, I assumed that order number 1028 might not be available in the Shopify store. To ensure the application's functionality, a decision was made to retrieve a list of available orders and use a different order number for demonstration purposes. 

### Hyperlink Navigation

To enhance user experience and facilitate navigation within the application, hyperlinks were utilized throughout the interface. The decision to use hyperlinks was made to make it easier for users to access different endpoints and functionalities of the application. This design choice aims to improve usability and streamline the interaction process for users interacting with the Shopify Data Handling App.
