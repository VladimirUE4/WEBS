# Sensor Data Visualization System

## Description
Système de visualisation de données de capteurs en temps réel, composé d'un daemon C++ pour la lecture des données et d'une interface web pour la visualisation. Le projet utilise Flask pour le backend et une interface web moderne avec AJAX pour les mises à jour en temps réel.

## Structure du Projet
project/
├── daemon/
│   ├── deamon.cpp      # Programme C++ pour lire les données des capteurs
│   └── Makefile        # Configuration de compilation
├── server/
│   ├── app.py          # Serveur Flask
│   ├── static/
│   └── templates/
│       └── index.html  # Interface web
└── sensor/
    ├── data/           # Fichiers de données CSV
    │   ├── subject1_activity0.csv
    │   ├── subject1_activity1.csv
    │   └── ...
    └── index/          # Fichiers d'index pour le suivi

## Prérequis
- Python 3.7+
- Flask
- G++ (compilateur C++)
- Make
- jQuery (inclus via CDN)

## Installation
1. Cloner le repository :
git clone [url-du-repo]
cd [nom-du-projet]

2. Compiler le daemon :
make

3. Installer les dépendances Python :
pip install flask

## Structure des Données
Les fichiers de données doivent être au format CSV avec la structure suivante :
timestamp,x,y,z
1234567890,0.1,0.2,0.3

## Démarrage
1. Démarrer le serveur Flask :
cd server
python app.py

2. Accéder à l'interface web :
http://localhost:5000

## Utilisation
1. Dans l'interface web :
   - Sélectionner un sujet (1-3)
   - Sélectionner une activité (0-4)
   - Cliquer sur "Initialize Daemon" pour démarrer la capture
   - Utiliser "Start Capture" pour commencer la visualisation
   - "Stop Capture" pour arrêter
   - "Clear Console" pour nettoyer l'affichage

## Fonctionnalités
- Interface console stylisée en vert sur noir
- Sélection dynamique des sujets et activités
- Visualisation en temps réel des données
- Auto-scroll des données
- Gestion des erreurs
- Sauvegarde de l'index de lecture

## Architecture Technique

### Backend
- Daemon (C++)
  - Lecture des fichiers CSV
  - Gestion des index de lecture
  - Envoi des données ligne par ligne
  - Gestion des signaux d'interruption

- Serveur Flask (Python)
  - Gestion des requêtes HTTP
  - Communication avec le daemon
  - Parsing des données CSV
  - API REST pour les données en temps réel

### Frontend
- Interface Web
  - Design console rétro
  - Requêtes AJAX pour les mises à jour en temps réel
  - Auto-scroll des données
  - Gestion des erreurs utilisateur

## Communication
- Client → Serveur : Requêtes AJAX (GET/POST)
- Serveur → Daemon : Communication via stdout/stderr
- Daemon → Fichier : Lecture CSV et gestion des index

## Gestion des Erreurs
- Vérification de l'existence des fichiers
- Gestion des interruptions du daemon
- Affichage des erreurs dans l'interface
- Sauvegarde de l'état en cas d'arrêt


## Licence
MIT License
