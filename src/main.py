import os
from cloud_storage_bucket import CloudStorageBucket
from image_text_extractor import ImageTextExtractor
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from plaque_db import PlaqueDB
from PIL import Image
import os
import uuid
import shlex

def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()

def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging

def get_coordinates(geotags):
    if not geotags:
        return None

    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])
    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat, lon)

def get_decimal_from_dms(dms, ref):
    degrees = dms[0]
    minutes = dms[1] / 60.0
    seconds = dms[2] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return degrees + minutes + seconds

# create a method that will convert any heic files to jpeg using imagemagick and delete the original files

def convert_heic_to_jpeg():
    print("Converting HEIC files to JPEG")
    
    # Directory containing the photos
    photo_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'photos')
    
    # Iterate over each photo
    for photo in os.listdir(photo_dir):
        
        # if the file isn't a photo file then skip
        if not photo.lower().endswith(('heic', 'heif')):
            continue
        
        # Full path of the photo
        photo_path = os.path.join(os.getcwd(), 'data/photos/', photo)
        
        # print that we are processing the photo
        print(f'Converting {photo_path} to jpeg')
        
        # change photo_path to remove the heic extension
        new_photo_path = os.path.splitext(photo_path)[0] + '.jpeg'
        
        # escape the paths for shell execution
        escaped_photo_path = shlex.quote(photo_path)
        escaped_new_photo_path = shlex.quote(new_photo_path)
        
        # convert the photo to jpeg
        os.system(f'magick convert {escaped_photo_path} {escaped_new_photo_path}')
        
        # delete the original photo
        os.system(f'rm {escaped_photo_path}')

def main():
    # Directory containing the photos
    photo_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'photos')
    
    convert_heic_to_jpeg()
    
    extractor = ImageTextExtractor()
    cloud_storage_bucket = CloudStorageBucket()
    cloud_storage_bucket.delete_all_files()
    
    # List to store location data
    ids = []
    locations = []
    images = []
    bearings = []
    texts = []

    # Iterate over each photo
    for photo in os.listdir(photo_dir):
        
        # if the file isn't a photo file then skip
        if not photo.endswith('jpeg'):
            print(f'Skipping {photo}')
            continue
        
        # Full path of the photo
        photo_path = os.path.join(os.getcwd(), 'data/photos/', photo)
        
        # print that we are processing the photo
        print(f'Processing {photo_path}')
        
        
        try:
            # read the location data
            exif = get_exif(photo_path)
            geotags = get_geotagging(exif)
            coordinates = get_coordinates(geotags)
            bearing = int(geotags['GPSImgDirection'])
            
            locations.append(coordinates)
            
            bearings.append(bearing)
        except Exception as e:
            print(f"Failed to read exif data for {photo_path}, skipping : {e}")
            continue
        
        uuid_str = str(uuid.uuid4())
        ids.append(uuid_str)
        
        # upload the image to the bucket
        image_url = cloud_storage_bucket.upload_file(photo_path)
        
        # append the image to the list of images
        images.append(image_url)

        # extract the text from the photo
        text = extractor.extract_text_from_image(photo_path)
        texts.append(text)
    
        
    
    # call cloud search to insert the data into the index
    plaqueDB = PlaqueDB()
    plaqueDB.reset_data()
    
    plaqueDB.insert_into_index(ids, texts, images, locations, bearings)   
    print("Done")

if __name__ == "__main__":
    
    main()