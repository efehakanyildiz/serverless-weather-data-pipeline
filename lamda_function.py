import json
import boto3
import urllib3
from datetime import datetime

def lambda_handler(event, context):
    # API configuration for coordinates
    lat = 41.1034
    lon = 28.9914
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    
    http = urllib3.PoolManager()
    
    try:
        # Fetch weather data
        response = http.request('GET', url)
        data = json.loads(response.data.decode('utf-8'))
        
        # Generate unique filename with timestamp
        now = datetime.now()
        file_name = f"raw_weather_data_{now.strftime('%Y%m%d_%H%M%S')}.json"
        
        # Upload to S3 bucket
        s3 = boto3.client('s3')
        bucket_name = 'efe-data-engineering-bronze' 
        
        s3.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=json.dumps(data)
        )
        
        print(f"Success: {file_name} uploaded to S3 bucket.")
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': f"File successfully saved: {file_name}"})
        }
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"An error occurred: {str(e)}"})
        }