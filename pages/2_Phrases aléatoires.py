from dotenv import load_dotenv
import streamlit as stm
import sys
import os
import openai
from essential_generators import DocumentGenerator
import time

stm.title("Génération de phrases aléatoires")
stm.sidebar.success("Visualisation du projet 2 - Phrases aléatoires")
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

model = "text-davinci-003"
max_tokens = 850
language = 'Française'

gen = DocumentGenerator()
stm.header("Avec DocumentGenerator")
stm.write(gen.sentence())

stm.header("Avec Chat-GPT")
keyword = stm.text_input("Veuillez saisir des mots clefs")
if len(keyword) == 0:
    stm.error("Veuillez saisir une valeur et appuyer sur la touche Entrée")
else:    
    btn = stm.button('Générer')
    if btn:     
        with stm.spinner(text="Génération en cours..."):
            time.sleep(5)   

        text_area = stm.empty()

        prompt = f"Génere 5 exemples de phrases aléatoires en langue {language} contenant le mot {keyword}. \
        Traduire chacune de ces 5 phrases en 3 langues différentes aléatoires. \
        Les exemples de phrases peuvent être de longueur moyenne ou longue. \
        Il faut afficher toutes les phrases en respectant le format d'affichage suivant :\
        |la langue de traduction : la phrase traduite \
        "

        response = openai.Completion.create(
            engine=model, 
            prompt=prompt, 
            max_tokens=max_tokens, 
            n=1, 
            stop=None, 
            temperature=0.4,
            top_p=1.0,
            frequency_penalty=0.3,
            presence_penalty=0.0,
        )
        text_reponse = text_area.text_area('Mot clef ' + "'" + keyword + "'",response["choices"][0]["text"].strip(),500)