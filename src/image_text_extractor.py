# create a class that has methods that will extract the text from the image using the google cloud vision apis
# Path: src/photo_analysis/text.py
from google.cloud import vision
from PIL import Image, ImageDraw
import io
import os
import sys

class ImageTextExtractor:
    def __init__(self):
        # Create a client
        self.client = vision.ImageAnnotatorClient()

    # create a method that extracts the x and y coordinates from a string of format (x,y)
    def coords(self, word):
        # split the string into an array of strings
        coordinates_array = coordinates.split(',')

        # extract the x and y coordinates from the array of strings
        x = coordinates_array[0]
        y = coordinates_array[1]

        # return the x and y coordinates
        return x, y
    
    def distance(self, word1, word2):
        # print(f"Vertices: {word1[1]}")
        # Calculate the center coordinates of word1
        x1 = (word1[1][0][0] + word1[1][2][0]) / 2
        y1 = (word1[1][0][1] + word1[1][2][1]) / 2

        # Calculate the center coordinates of word2
        x2 = (word2[1][0][0] + word2[1][2][0]) / 2
        y2 = (word2[1][0][1] + word2[1][2][1]) / 2

        # Calculate the distance between the centers of the bounding boxes
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

        return distance

    def group_words(self, words, threshold):
        groups = []
        for word in words:
            if not groups:
                groups.append([word])
            else:
                min_distance = float('inf')
                min_group = None
                for group in groups:
                    for group_word in group:
                        dist = self.distance(word, group_word)
                        if dist < min_distance:
                            min_distance = dist
                            min_group = group
                if min_distance < threshold:
                    min_group.append(word)
                else:
                    groups.append([word])
        return groups

    def extract_text_from_image(self, image_path):
        """
        Function to extract text from an image
        :param image_path: Path to the image file
        :return: Extracted text as a string
        """

        # Open the image
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        # For dense text, use document_text_detection
        # For less dense text, use text_detection
        response = self.client.text_detection(image=image)

        # create an array to store a tuple of the words and the bounds
        words = []

        for text in response.text_annotations:
            # ignore the first element in the array because it is the entire text
            if text.description == response.text_annotations[0].description:
                continue

            vertices = [(vertex.x, vertex.y)
                        for vertex in text.bounding_poly.vertices]
            
            # insert a tuple in to the words array with the text found and the bounds
            words.append((text.description, vertices))

        # iterate through the words array and find groupings of words that are in the same vertical line
        # create a new array to store the groupings of words
        groupings = self.group_words(words, 70)
            
        # iterate through the groupings and print the words in each grouping
        # print('Groupings:')
        grouped_text = []
        for grouping in groupings:
            current_group = ''
            for word in grouping:
                current_group += word[0] + ' '
                
            grouped_text.append(current_group)
        
        return grouped_text
