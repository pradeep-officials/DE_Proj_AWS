import json
import boto3 

def lambda_handler(event, context):

    # Initialize the S3 client
    s3 = boto3.client('s3')
    
    def move_files(source_bucket, destination_bucket, source_prefix='', destination_prefix=''):
        # List all objects in the source bucket with the given prefix (folder)
        response = s3.list_objects_v2(Bucket=source_bucket, Prefix=source_prefix)
    
        # Check if there are files to move
        if 'Contents' in response:
            for file in response['Contents']:
                source_key = file['Key']
                
                # Skip any "folder marker" object. Only process actual files.
                if source_key.endswith('/'):  # <-- Skip if it's a folder marker
                    continue
                
                # Create the destination key by appending the source file to the destination prefix
                destination_key = destination_prefix + source_key.split('/')[-1]
                
                # Copy the file to the destination bucket
                s3.copy_object(CopySource={'Bucket': source_bucket, 'Key': source_key}, 
                               Bucket=destination_bucket, Key=destination_key)
                
                # Delete the source file after copying
                s3.delete_object(Bucket=source_bucket, Key=source_prefix + source_key.split('/')[-1])
                print(f"Moved {source_key} to {destination_key}")
        else:
            print(f"No files found with prefix {source_prefix}")
    
    # Define source and destination buckets and prefixes
    source_bucket = 'spotify-etl-pipeline-cm'
    destination_bucket = 'spotify-etl-pipeline-cm'
    
    # Prefixes (folders)
    source_prefix = 'raw_data/bronze/'
    destination_prefix = 'raw_data/processed-archive/'
    
    # Move files from 'raw_data/bronze/' to 'raw_data/processed-archive/'
    move_files(source_bucket, destination_bucket, source_prefix, destination_prefix)
