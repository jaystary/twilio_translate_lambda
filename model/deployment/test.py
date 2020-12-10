import os

import six
from google.cloud import translate_v2 as translate

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "model/deployment/creds.json"

def run_this():
    body = {}
    body['src'] = "de"
    body['dest'] = "es"
    body ['input'] = "Hallo"
    
    #Infere API - hook your only model etc....
    
    translate_client = translate.Client()

    if isinstance(body['src'], six.binary_type):
        text = body['src'].decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(body['input'], 
                                        target_language=body['dest'],
                                        source_language=body['src'], 
                                        model="nmt")
    print("x")

run_this()