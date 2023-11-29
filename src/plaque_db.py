# create a class that has methods to insert into a google cloud search index as well as search the index. The data should be searchable by text and should return a location and image path from the text
# Path: src/cloud_search.py
from google.cloud import vision
from google.cloud import bigquery
from PIL import Image, ImageDraw
from google.cloud import bigquery

class PlaqueDB:
    def __init__(self):
        # Create a client
        self.client = bigquery.Client()

    def reset_data(self):
        # Run a query
        query = """
            DELETE FROM `csp-plaques.plaques.plaques` WHERE TRUE
        """
        query_job = self.client.query(query)
        # query_job.result()  # Wait for the query to complete

    def insert_into_index(self, ids, texts, images, locations, bearings):
        """
        Function to extract text from an image and insert it into a google cloud search index
        :param image_path: Path to the image file
        :return: Extracted text as a string
        """

        print("Text values: ", texts)
        data_to_insert = [
            {"id": id, "text": text, "image_url": image,
                "latitude": location[0], "longitude": location[1], "bearing": bearing}
            for id, text, image, location, bearing in zip(ids, texts, images, locations, bearings)]

        # Define your table ID
        table_id = "csp-plaques.plaques.plaques"

        # Use the client to insert data into the table
        errors = self.client.insert_rows_json(table_id, data_to_insert)

        # Check if any errors occurred
        if errors == []:
            print("New rows have been added.")
        else:
            print("Errors occurred:", errors)
