/**
 * Daemon de capture de données de capteurs
 * Ce programme lit les données d'un fichier CSV contenant des mesures de capteurs
 * et les affiche de manière continue avec un délai entre chaque ligne
 */

#include <fstream>      // Pour la lecture de fichiers
#include <sstream>      // Pour la manipulation de chaînes
#include <string.h>
#include <iostream>
#include <iomanip>
#include <vector>
#include <algorithm>
#include <csignal>     // Pour la gestion des signaux (Ctrl+C)
#include <chrono>      // Pour la gestion du temps
#include <thread>      // Pour sleep_for
#include <mutex>

// Variables globales
const std::string dirPrefix = {"sensor/"};  // Préfixe du chemin des fichiers
std::string subject;                        // Identifiant du sujet
int my_sId;                                // ID du sujet
int my_activity;                           // ID de l'activité
int my_index;                              // Index de lecture actuel

/**
 * Sauvegarde l'index d'itération dans un fichier
 * Permet de reprendre la lecture là où on s'était arrêté
 */
void setIterationIndex(std::string fname){
    std::stringstream ss;
    ss << dirPrefix << "/index/" << fname << "_activity"<< my_activity << ".idx";
    std::string filename = ss.str();  
    std::ofstream ofile;
    ofile.open(filename);
    ofile << my_index;
    ofile.close();
}

/**
 * Lecture de l'index d'itération depuis le fichier
 * Si le fichier n'existe pas, commence à l'index 1
 */
void getIterationIndex(std::string fname){
    my_index = 1;
    std::stringstream ss;
    ss << dirPrefix << "/index/" << fname << "_activity"<< my_activity << ".idx";
    std::string filename = ss.str();

    std::ifstream ifile;
    ifile.open(filename);
    
    if (ifile){
        std::string line;
        std::getline (ifile, line);
        my_index = atoi(line.c_str());
        ifile.close();
    }
}

/**
 * Gestionnaire de signal pour Ctrl+C
 * Sauvegarde l'index avant de quitter
 */
void signal_handler(int signal){
    setIterationIndex(subject);
    exit(1);
}

/**
 * Fonction principale
 * Args:
 *   argv[1]: ID du sujet
 *   argv[2]: ID de l'activité
 */
int main(int argc, char *argv[]){
    // Initialisation des variables
    my_sId = 0;
    my_activity = 0;
    my_index = 1;
    subject.append("subject");

    // Installation du gestionnaire de signal pour Ctrl+C
    std::signal(SIGINT, signal_handler);
    
    // Récupération des arguments
    if (argc > 2 && argv[0] != ""){
        my_sId = atoi(argv[1]);      // ID du sujet
        my_activity = atoi(argv[2]);  // ID de l'activité
    }
    subject.append(std::to_string(my_sId));
    
    // Récupération de l'index de lecture
    getIterationIndex(subject);    
    
    // Construction du chemin du fichier de données
    std::stringstream ss;
    ss << dirPrefix << "data/" << subject << "_activity" << my_activity << ".csv";
    std::string filename = ss.str();
    std::ifstream input(filename);

    // Vérification de l'ouverture du fichier
    if (!input.is_open()){
        std::cerr << "Erreur de lecture du fichier : " << filename << "\n";
        return 1; 
    }

    // Lecture de l'en-tête du CSV
    std::string line;
    std::getline(input, line);  // Skip first line (header)

    // Boucle principale de lecture des données
    while(true) {
        if(std::getline(input, line)) {
            // Affichage de la ligne et pause
            std::cout << line << std::endl;
            std::this_thread::sleep_for(std::chrono::milliseconds(50));
        } else {
            // Retour au début du fichier quand on atteint la fin
            input.clear();
            input.seekg(0);
            std::getline(input, line);  // Skip header again
        }
    }

    return 0;
}
