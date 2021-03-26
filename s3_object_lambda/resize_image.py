'''
Purpose:
	Resize Image to half of original size.
'''
import boto3
import requests
import io
from PIL import Image

def lambda_handler(event, context):
    print(event)

    object_get_context = event["getObjectContext"]
    request_route = object_get_context["outputRoute"]
    request_token = object_get_context["outputToken"]
    s3_url = object_get_context["inputS3Url"]
    in_mem_file = io.BytesIO()

    # get object from s3
    response = requests.get(s3_url)
    original_object = Image.open(io.BytesIO(response.content))

    transformed_object = original_object.resize(
        (original_object.size[0] // 2, original_object.size[1] // 2))
    transformed_object.save(in_mem_file, format=original_object.format)

    # Write object back to S3 Object Lambda
    s3 = boto3.client('s3')
    s3.write_get_object_response(
        Body=in_mem_file.getvalue(),
        RequestRoute=request_route,
        RequestToken=request_token)

    return {'status_code': 200}
