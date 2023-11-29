# create a method to extract the location from the exif data of the photo
# Path: src/photo_analysis/location.py
import exifread

def extract_location_from_exif(image_path):
    """
    Function to extract the location from the exif data of the photo
    :param image_path: Path to the image file
    :return: Extracted location as a string
    """
    # Open image file for reading (binary mode)
    f = open(image_path, 'rb')

    # Return Exif tags
    tags = exifread.process_file(f)

    # print the tags for debugging
    print(f"Tags: {tags}")
    
    # Close image file
    f.close()

    # Check if GPS data is present
    if 'GPS GPSLongitude' in tags:
        # Get the longitude and convert it to a string
        longitude = str(tags['GPS GPSLongitude'])

        # Get the latitude and convert it to a string
        latitude = str(tags['GPS GPSLatitude'])

        # Get the latitude reference and convert it to a string
        latitude_ref = str(tags['GPS GPSLatitudeRef'])

        # Get the longitude reference and convert it to a string
        longitude_ref = str(tags['GPS GPSLongitudeRef'])

        # Return the extracted location
        return f'{latitude},{latitude_ref},{longitude},{longitude_ref}'
    else:
        # Return empty string if GPS data is not present
        return ''