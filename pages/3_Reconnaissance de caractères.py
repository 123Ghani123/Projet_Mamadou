from dotenv import load_dotenv
import streamlit as stm 
import requests, os, time
import requests
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes

stm.title("Reconnaissance de caractères - OCR")
stm.sidebar.success("Visualisation du projet 3 - Reconnaissance de caractères")

load_dotenv()
key = os.getenv('KEY')
region = os.getenv('REGION')
endpoint = os.getenv('ENDPOINT')
COG_key = os.getenv('COG_KEY')
COG_region = os.getenv('COG_REGION')
COG_endpoint = os.getenv('COG_ENDPOINT')

def get_text(image_url, computervision_client):
    # Open local image file
    read_response = computervision_client.read(image_url, raw=True)

    # Get the operation location (URL with an ID at the end)
    read_operation_location = read_response.headers["Operation-Location"]
    # Grab the ID from the URL
    operation_id = read_operation_location.split("/")[-1]

    # Retrieve the results 
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status.lower() not in ["notstarted", "running"]:
            break
        time.sleep(1)

    # Get the detected text
    text = ""
    if read_result.status == OperationStatusCodes.succeeded:
        for page in read_result.analyze_result.read_results:
            for line in page.lines:
                # Get text in each detected line and do some fixes to the structure
                if (not text) or text[-1].strip() == "." or text[-1].strip() == ":":
                    text = text + "\n" + line.text
                else:
                    text = text + " " + line.text
    text = text.replace(" .", ".").replace(" ,", ",").replace(" :", ":")
    return text

def detect_language(text, key, region, endpoint):
    # Use the Translator detect function
    path = "/detect"
    url = endpoint + path
    # Build the request
    params = {
        "api-version": "3.0"
    }
    headers = {
    "Ocp-Apim-Subscription-Key": key,
    "Ocp-Apim-Subscription-Region": region,
    "Content-type": "application/json"
    }
    body = [{
        "text": text
    }]
    # Send the request and get response
    request = requests.post(url, params=params, headers=headers, json=body)
    response = request.json()
    # Get language
    language = response[0]["language"]
    # Return the language
    return language

def translate(text, source_language, target_language, key, region, endpoint):
    # Use the Translator translate function
    url = endpoint + "/translate"
    # Build the request
    params = {
        "api-version": "3.0",
        "from": source_language,
        "to": target_language
    }
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-type": "application/json"
    }
    body = [{
        "text": text
    }]
    # Send the request and get response
    request = requests.post(url, params=params, headers=headers, json=body)
    response = request.json()
    # Get translation
    translation = response[0]["translations"][0]["text"]
    # Return the translation
    return translation

if __name__ == '__main__':
    ma_liste = {'Anglais': 'en', 'Francais': 'fr', 'Italien': 'it', 'Allemand': 'de', 'Japonnais': 'ja'}    
    image_url = stm.text_input("Veuillez saisir l'URL de l'image à analyser","https://zestedesavoir.com/media/galleries/732/81bdc1c4-fdcc-453f-ad71-c2a9ad19fcc4.png")
    selected_option = stm.selectbox('Sélectionnez la langue de traduction', list(ma_liste.keys()))
    target_language = ma_liste[selected_option]
    if len(image_url) == 0:
        stm.error("Veuillez saisir une URL et appuyer sur la touche Entrée")
    else:
        btn = stm.button('Extraire')
        if btn:     
            with stm.spinner(text="Extraction en cours..."):
                time.sleep(5) 

            # Authenticate Computer Vision client
            computervision_client = ComputerVisionClient(COG_endpoint, CognitiveServicesCredentials(COG_key))
            # Extract text
            text = get_text(image_url, computervision_client)
            # Detect language
            language = detect_language(text, key, region, endpoint)
            # Translate text
            translated_text = translate(text, language, target_language, key, region, endpoint)

            stm.text_area("Texte original",text,200)
            stm.text_area("Texte Traduit en " + selected_option,translated_text,200)            