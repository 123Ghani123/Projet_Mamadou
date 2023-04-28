from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speechsdk
import requests,uuid
import json
import streamlit as stm

stm.title("Application de reconnaissance vocale et de traduction")
stm.sidebar.success("Visualisation du projet 1 - Reconnaissance Vocale")

# Configuration des clés et des endpoints de l'API
load_dotenv()
speech_key = os.getenv('SPEECH_KEY')
service_region = os.getenv('REGION')
translation_key = os.getenv('KEY')
translation_endpoint = os.getenv('TRANSLATION_ENDPOINT')

def recognize_speech_from_microphone():
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_recognition_language="fr-FR"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    return speech_recognizer.recognize_once_async().get()

    # if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
    #     print("Recognized: {}".format(speech_recognition_result.text))
    # elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
    #     print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    # elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
    #     cancellation_details = speech_recognition_result.cancellation_details
    #     print("Speech Recognition canceled: {}".format(cancellation_details.reason))
    #     if cancellation_details.reason == speechsdk.CancellationReason.Error:
    #         print("Error details: {}".format(cancellation_details.error_details))
    #         print("Did you set the speech resource key and region values?")

# Fonction pour la traduction de texte
def translate_text(text, target_language):
    headers = {
        "Ocp-Apim-Subscription-Key": translation_key,
        'Ocp-Apim-Subscription-Region': service_region,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4())
    }
    params = {
        "api-version": "3.0",
        "from": "fr",
        "to": target_language
    }
    body = [{
        "text": text
    }]
    request = requests.post(translation_endpoint, headers=headers, params=params, json=body)
    response = request.json()

    return json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': '))

# Exemple d'utilisation de la reconnaissance vocale et de la traduction
if __name__ == "__main__":
    ma_liste = {'Anglais': 'en', 'Francais': 'fr', 'Italien': 'it', 'Allemand': 'de', 'Japonnais': 'ja'}        
    selected_option = stm.selectbox('Sélectionnez la langue de traduction', list(ma_liste.keys()))
    target_language = ma_liste[selected_option]

    stm.write("Parlez en Francais dans le microphone et l'application traduira votre voix dans la langue sélectionnée.")
    # Bouton pour lancer la reconnaissance vocale
    if stm.button("Démarrer la reconnaissance vocale"):
        result = recognize_speech_from_microphone()
        stm.write("Enregistrement en cours...")
       # Traduction        
        data = json.loads(translate_text(result.text, target_language))
        translated_text = data[0]['translations'][0]['text']
        # affichage des resultats
        stm.write("Vous avez dit : {}".format(result.text))
        stm.write("Traduction en {}: {}".format(target_language, translated_text))
