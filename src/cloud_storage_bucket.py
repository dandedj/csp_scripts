from google.cloud import storage
from google.oauth2 import service_account

class CloudStorageBucket:
    def __init__(self):
        # set the bucket name
        self.bucket_name = 'csp-bucket'

        # set the project id
        self.project_id = 'csp-plaques'

        # create a storage client
        self.client = storage.Client(
            project=self.project_id)

        # create the bucket
        self.bucket = self.client.get_bucket(self.bucket_name)

    def upload_file(self, file_path):
        # upload the file to the bucket
        # extract the last part of the file path to be used for the blob name
        file_name = file_path.split('/')[-1]

        file_blob = self.bucket.blob(file_name)
        file_blob.upload_from_filename(file_path)

        # get the url of the file
        url = file_blob.public_url

        return url

    def download_file(self, file_path):
        # download the file from the bucket
        file_blob = self.bucket.blob(file_path)
        file_blob.download_to_filename(file_path)

        return file_path

    def delete_file(self, file_path):
        # delete the file from the bucket
        file_blob = self.bucket.blob(file_path)
        file_blob.delete()

    def list_files(self):
        # list the files in the bucket
        files = self.client.list_blobs(self.bucket_name)

        return files

    # add a new method to delete all images from the bucket
    def delete_all_files(self):
        # list all of the blobs in the bucket
        blobs = self.client.list_blobs(self.bucket_name)

        # iterate over each blob and delete it
        for blob in blobs:
            blob.delete()
