import os
import json
import six
from twilio.rest import Client
from google.cloud import translate_v2 as translate

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "creds.json"

def lambdaHandler(event, context):
    
    account_sid = "twilio sid"
    auth_token  = "twilio token"
    method = event['requestContext']['http']['method']
    path = event['rawPath']    
    body=json.loads(event['body'])    
    
    if method == 'POST' and path == '/messages/':  
       
        #Infere API - hook your only model etc....
        translate_client = translate.Client()

        if isinstance(body['src'], six.binary_type):
            text = body['src'].decode("utf-8")

        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.

        if isinstance(body['src'], six.binary_type):
            text = body['src'].decode("utf-8")

        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.
        result = translate_client.translate(body['input'], 
                                            target_language=body['dest'],
                                            source_language=body['src'], 
                                            model="nmt")
        
        '''
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            to=body['to'], 
            from_="+18047350925",
            body=body['input'])
            print(message.sid)
        '''        

        return {'body': result["translatedText"], 'statusCode': 200}
    
    return {'body': "", 'statusCode': 404}

