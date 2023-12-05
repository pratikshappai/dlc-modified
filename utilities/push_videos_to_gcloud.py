# load gcloud api keys
from google.oauth2 import service_account
from google.cloud import storage

key_path = '/path/to/your/key.json'
scopes = ['https://www.googleapis.com/auth/cloud-platform']
creds = service_account.Credentials.from_service_account_file(
    key_path, scopes=scopes)

client = storage.Client(credentials=creds)
buckets = client.list_buckets()

for bucket in buckets:
    print(bucket.name)


# check the folders 2023-* for any changes in the file 


# if there are changes, then push the files to gcloud bucket
