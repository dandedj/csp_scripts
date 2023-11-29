from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import sys

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

# set the filename to the first parameter passed to the script
filename = sys.argv[1]

exif = get_exif(filename)
geotags = get_geotagging(exif)
coordinates = get_coordinates(geotags)

# print out all of the information to be viewed in the terminal

print(f"Filename: {filename}")
print(f"EXIF: {exif}")
print(f"Geotags: {geotags}")
print(f"Coordinates: {coordinates}")

# print out the coordinates in a format that can be used in the map_plot.py file

print(f"Coordinates for map_plot.py: {coordinates[0]}, {coordinates[1]}")
