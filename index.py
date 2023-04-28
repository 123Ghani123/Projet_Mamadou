import streamlit as stm


stm.set_page_config(page_title = "Projets API")
stm.title("MEZZI Ghani - Projets API - Simplon")
stm.markdown(
"""
**Projet 1: Reconnaissance Vocale - Speech To Text :**
- Choisir la langue de traduction
- Démarrer l'enregistrement et parler en Francais
- La traduction se fera dès que vous aurez finis de parler
"""
)

stm.markdown(
"""
**Projet 2: Génération de phrases aléatoires :**
- Saisir des mots clefs en français qui doivent apparaitre dans les phrases
- 5 phrases seront générées et traduites dans des langues choisies aléatoirement
"""
)

stm.markdown(
"""
**Projet 3: Reconnaissance de caractères - OCR :**
- Saisir une URL qui pointe vers une image contenant du texte
- Sélectionner la langue de traduction
- L'application détecte automatiquement la langue de l'image et applique la traduction 
"""
)

stm.sidebar.success("Veuillez sélectionner un des 3 projets")