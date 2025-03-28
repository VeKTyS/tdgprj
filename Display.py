import os
import ast
import numpy as np
from tabulate import tabulate
from Table import* 
from Caluls import* 

def analyze_schedule(constrain_table):
    table = constrain_table_reader(constrain_table)
    tasks, durations, constraints = table
    
    # Calcul des dates au plus tôt
    earliest = earliest_dates(tasks, durations, constraints)
    project_end = max(earliest.values())
    
    # Calcul des dates au plus tard
    latest = latest_dates(tasks, durations, constraints, project_end)
    
    # Calcul des marges
    margins = compute_margins(earliest, latest)
    
    # Identification des tâches critiques
    critical_path_tasks = critical_paths(margins)
    
    # Obtenir les prédécesseurs et successeurs
    predecessors = get_predecessors(tasks, constraints)
    successors = get_successors(tasks, constraints)
    
    def calculate_ranks(tasks, predecessors):
        ranks = {task: 0 for task in tasks}  # Initialisation des rangs à 0
        
        # Parcours des tâches dans l'ordre des dépendances
        for task in tasks:
            if predecessors[task]:  # Si la tâche a des prédécesseurs
                ranks[task] = 1 + max(ranks[pred] for pred in predecessors[task])
        
        return ranks

    ranks = calculate_ranks(tasks, predecessors)
    
    # Préparation des données pour l'affichage
    headers = ["Propriété"] + tasks
    schedule_data = [
        ["Prédécesseurs"] + [", ".join(predecessors[task]) if predecessors[task] else "-" for task in tasks],
        ["Successeurs"] + [", ".join(successors[task]) if successors[task] else "-" for task in tasks],
        ["Date au plus tôt"] + [earliest[task] for task in tasks],
        ["Date au plus tard"] + [latest[task] for task in tasks],
        ["Marge"] + [margins[task] for task in tasks],
        ["Chemin critique"] + ["Oui" if task in critical_path_tasks else "Non" for task in tasks],
        ["Rang"] + [ranks[task] for task in tasks]
    ]
    
    # Affichage des résultats sous forme de tableau horizontal
    print("\nAnalyse de l'ordonnancement :")
    print(tabulate(schedule_data, headers=headers, tablefmt="grid"))
    
    # Trouver les chemins critiques complets
    def find_critical_paths(task, path, critical_path_tasks, successors):
        if task not in critical_path_tasks:
            return []
        if not successors[task]:  # Si la tâche n'a pas de successeurs
            return [path + [task]]
        paths = []
        for succ in successors[task]:
            if succ in critical_path_tasks:
                paths.extend(find_critical_paths(succ, path + [task], critical_path_tasks, successors))
        return paths

    critical_paths_list = []  # Liste des chemins critiques
    for task in tasks:
        if task in critical_path_tasks and not predecessors[task]:  # Tâches de départ critiques
            critical_paths_list.extend(find_critical_paths(task, [], critical_path_tasks, successors))
    
    # Affichage des chemins critiques
    print("\nChemins critiques :")
    for path in critical_paths_list:
        print(" -> ".join(path))
    
    return earliest, latest, margins, critical_paths_list, ranks

def display_graph(constrain_table):
    table = constrain_table_reader(constrain_table)
    tasks, durations, constraints = table
    N = len(tasks) # Nombre de tâches 
    graph = np.full((N + 2, N + 2), '*', dtype=object) # Matrice de valeurs
    
    for i, task in enumerate(tasks):  
        for constrained_task in constraints[i]:  # Chaque tâche dont i dépend
            if constrained_task in tasks:
                constrained_index = tasks.index(constrained_task)  # Trouver son index
                graph[i, constrained_index] = int(durations[constrained_index])  # Associer la bonne durée

    # Transpose the graph matrix
    graph = graph.T

    # Création des en-têtes
    headers = ['0'] + [chr(65 + i) for i in range(N-2)] + [str(N-1)]

    # Affichage des en-têtes avec alignement
    print("    " + " ".join(f"{h:>3}" for h in headers))
    for i in range(N):
        row = []
        for j in range(N):
            row.append(f"{graph[i, j]:>3}")
        print(f"{headers[i]:>3} " + " ".join(row))

    successors = get_successors(tasks, constraints)
    #print("\nSuccesseurs des tâches :")
    #for task, succ in successors.items():
        #print(f"Tâche {task}: {', '.join(succ) if succ else 'Aucun successeur'}")    

    predecessors = get_predecessors(tasks, constraints)
    #print("\nPrédécesseurs des tâches :")
    #for task, pred in predecessors.items():
        #print(f"Tâche {task}: {', '.join(pred) if pred else 'Aucun prédécesseur'}")

    # Vérification des propriétés du graphe
    graph_dict = {task: successors[task] for task in tasks}
    if has_no_cycles(graph_dict) and has_no_negative_arcs(graph):
        print("\nLe graphe ne contient pas de cycles.")
        print("Le graphe ne contient pas d'arcs à valeur négative.")
        print("-> C'est un graphe d'ordonnancement\n")
        analyze_schedule(constrain_table)
    else:
        if not has_no_cycles(graph_dict):
            print("\nLe graphe contient des cycles.")
        else:
            print("Le graphe ne contient pas de cycles.")
        if not has_no_negative_arcs(graph):
            print("Le graphe contient des arcs à valeur négative.")
        else:
            print("Le graphe ne contient pas d'arcs à valeur négative.")
        print("-> Ce n'est pas un graphe d'ordonnancement\n")

    return graph

def clear_screen():
    """Efface l'écran de la console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    """Affiche le menu principal."""
    print("\nMenu Principal")
    print("1. Analyser une table spécifique")
    print("2. Analyser toutes les tables")
    print("3. Afficher le graphe d'une table")
    print("4. Quitter")

def get_table_path(directory, table_number):
    """Récupère le chemin du fichier de table correspondant au numéro donné (de table 1.txt à table 14.txt) dans le dossier 'contraintes'."""
    file_name = f"table {table_number}.txt"
    table_path = os.path.join(directory, "contraintes", file_name)
    if os.path.exists(table_path):
        return table_path
    else:
        print("Numéro de table invalide.")
        return None


def process_table(directory):
    """Demande un numéro de table et analyse la table correspondante."""
    table_number = input("Entrez le numéro de la table : ")
    table_path = get_table_path(directory, table_number)
    if table_path:
        print(f"\nAnalyse de la table : {table_path}")
        analyze_schedule(table_path)

def process_all_tables(directory):
    """Analyse toutes les tables dans un répertoire donné."""
    print("\nAnalyse de toutes les tables du répertoire...")
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".txt"):
            process_table(os.path.join(directory, filename))

def display_graph(directory):
    """Demande un numéro de table et affiche le graphe correspondant."""
    table_number = input("Entrez le numéro de la table : ")
    table_path = get_table_path(directory, table_number)
    if table_path:
        print(f"\nAffichage du graphe pour : {table_path}")
        display_graph(table_path)