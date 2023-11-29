# CSP Scripts

This project contains the scripts needed to ingest a series of photos and upload them to 
google cloud and populate a BigQuery database with the photos and metadata. 

The client code can be found at [csp_client](https://github.com/dandedj/csp_client)
The server code can be found at [csp_server](https://github.com/dandedj/csp_client)

## Getting Started

Must have python 3 or greater. 
Must pip install all needed modules

Must have a credentials file loaded into your home directory as ./csp_creds.json

## Running

Photos should be placed into the data/photos directory. 

Run the ingester by using 
python src/main.py