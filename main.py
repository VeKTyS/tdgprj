import os
import ast
import numpy as np
from tabulate import tabulate
from Display import* 
from Table import* 
from Caluls import* 

# Import de la table test pour création du fichier mémoire test
#constrain_table = "contraintes/table 2.txt"
#constrain_table_reader(constrain_table)

# Display graphe table test en mémoire
#print("Graph matrix:") 
#display_graph("memoire/table 2.txt")

import os
from display_functions import clear_screen, display_menu, process_table, process_all_tables, display_graph

if __name__ == "__main__":
    directory = input("Entrez le répertoire contenant les fichiers de contrainte : ")
    constraints_dir = os.path.join(directory, "contraintes")
    memory_dir = os.path.join(directory, "mémoire")  # Dossier mémoire
    
    if not os.path.exists(constraints_dir):
        print("Dossier 'contraintes' introuvable.")
    elif not os.path.exists(memory_dir):
        print("Dossier 'mémoire' introuvable. Création du dossier.")
        os.makedirs(memory_dir)  # Création du dossier mémoire si nécessaire
    else:
        while True:
            clear_screen()
            display_menu()
            choice = input("Choisissez une option : ")
            
            if choice == "1":
                table_number = input("Entrez le numéro de la table (1-14) : ")
                table_path = os.path.join(constraints_dir, f"table {table_number}.txt")
                if os.path.exists(table_path):
                    process_table(table_path)
                else:
                    print("Numéro de table invalide.")
            elif choice == "2":
                process_all_tables(constraints_dir)
            elif choice == "3":
                table_number = input("Entrez le numéro de la table (1-14) : ")
                table_path = os.path.join(constraints_dir, f"table {table_number}.txt")
                if os.path.exists(table_path):
                    display_graph(table_path)
                else:
                    print("Numéro de table invalide.")
            elif choice == "4":
                print("Fermeture du programme.")
                break
            else:
                print("Option invalide. Veuillez réessayer.")
            
            input("Appuyez sur Entrée pour continuer...")
