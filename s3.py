import boto3

BUCKET_NAME = '889307001689bucket'
ACCESS_ID = 'AKIA46DWT6NMT4CPN7OO'
ACCESS_KEY = 'UfMEqu2/cvu+cSV+nEtNHXvz8F0bImpDQbmASdZt'

s3 = boto3.resource('s3',
        aws_access_key_id=ACCESS_ID,
        aws_secret_access_key= ACCESS_KEY)


data = open('./data/data-2023-01-23.csv', 'rb')
s3.Bucket(BUCKET_NAME).put_object(Key='data-2023-01-23.csv', Body=data)