"""
Serveur Flask pour l'interface web de visualisation des données de capteurs
Ce serveur fait le lien entre l'interface web et le daemon C++
"""

from flask import Flask, render_template, jsonify, request
import socket
import threading
import csv
from io import StringIO
import subprocess
import os
import time

app = Flask(__name__)

DAEMON_HOST = 'localhost'
DAEMON_PORT = 8089
DAEMON_PROCESS = None  # Process du daemon en cours d'exécution

def parse_csv_line(line):
    """
    Parse une ligne CSV en dictionnaire
    Format attendu: timestamp,x,y,z
    """
    try:
        csv_reader = csv.reader(StringIO(line))
        row = next(csv_reader, None)
        if row:
            return {
                "timestamp": row[0] if len(row) > 0 else "",
                "x": row[1] if len(row) > 1 else "",
                "y": row[2] if len(row) > 2 else "",
                "z": row[3] if len(row) > 3 else ""
            }
    except Exception as e:
        print(f"Error parsing CSV: {str(e)}")
    return None

def get_sensor_data():
    """
    Récupère les données du daemon
    Retourne un dictionnaire avec les données ou une erreur
    """
    try:
        if DAEMON_PROCESS is None:
            return {"error": "Daemon not running"}
            
        # Vérifier si le processus est toujours en cours
        if DAEMON_PROCESS.poll() is not None:
            return {"error": "Daemon has stopped"}
            
        # Lire la sortie du daemon
        line = DAEMON_PROCESS.stdout.readline().strip()
        print(f"Raw line from daemon: '{line}'")  # Debug
        
        if not line:
            return {"error": "No data available"}
            
        parsed_data = parse_csv_line(line)
        if parsed_data:
            return parsed_data
        return {"error": "Failed to parse data"}
            
    except Exception as e:
        print(f"Error reading daemon output: {str(e)}")
        return {"error": str(e)}

@app.route('/')
def index():
    """Route principale - affiche l'interface web"""
    return render_template('index.html')

@app.route('/start_daemon', methods=['POST'])
def start_daemon():
    """
    Démarre le daemon avec les paramètres spécifiés
    Paramètres POST attendus:
    - subject: ID du sujet
    - activity: ID de l'activité
    """
    global DAEMON_PROCESS
    
    # Arrêt du daemon existant si nécessaire
    if DAEMON_PROCESS is not None:
        try:
            DAEMON_PROCESS.terminate()
            DAEMON_PROCESS.wait(timeout=2)
        except:
            pass
    
    subject = request.form.get('subject', '1')
    activity = request.form.get('activity', '0')
    
    try:
        # Chemin absolu vers le daemon
        daemon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'daemon')
        if os.name == 'nt':  # Windows
            daemon_path += '.exe'
            
        print(f"Starting daemon: {daemon_path} {subject} {activity}")  # Debug
        
        # Démarrer le daemon avec capture de sortie
        DAEMON_PROCESS = subprocess.Popen(
            [daemon_path, subject, activity],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
            cwd=os.path.dirname(daemon_path)  # Définir le répertoire de travail
        )
        
        # Attendre un peu pour s'assurer que le daemon démarre
        time.sleep(1)
        
        # Vérifier si le processus s'est terminé immédiatement (erreur)
        if DAEMON_PROCESS.poll() is not None:
            error = DAEMON_PROCESS.stderr.read()
            return jsonify({"status": "error", "message": f"Daemon failed to start: {error}"})
            
        return jsonify({"status": "success", "message": f"Daemon started with subject {subject} activity {activity}"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/data')
def get_data():
    """Route API pour récupérer les données actuelles du daemon"""
    data = get_sensor_data()
    print(f"Sending data: {data}")  # Debug
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000) 