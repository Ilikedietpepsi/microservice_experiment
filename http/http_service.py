# my_service.py
import json

from nameko.rpc import rpc
from nameko.web.handlers import http
import mysql.connector

class HttpService:
    name = "http_service"

    # Define an HTTP entrypoint to handle HTTP GET requests
    @http('GET', '/query')
    def handle_http_request(self):
        # Extract SQL query from the HTTP request parameters


        # Connect to your local MySQL database
        connection = mysql.connector.connect(
            host="mysql",
            user="root",
            password="hezhenmin2000",
            database="test"
        )

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor(dictionary=True)

        try:
            # Execute the SQL query
            cursor.execute("SELECT * FROM customer")

            # Fetch the results from the query
            results = cursor.fetchall()
            return 200, {'Content-Type': 'application/json'}, json.dumps({'result': str(results)})

        except mysql.connector.Error as error:
            # Handle any errors that may occur during execution
            return 500, {'Content-Type': 'application/json'}, json.dumps({'error': str(error)})

        finally:
            # Close the cursor and connection
            cursor.close()
            connection.close()


