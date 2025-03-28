import os
from datetime import datetime
import ast
import numpy as np
from tabulate import tabulate

def constrain_table_reader(constrain_table):
    memoire_dir = "memoire"
    memoire_file = os.path.join(memoire_dir, os.path.basename(constrain_table))
    
    # Create memoire directory if it doesn't exist
    if not os.path.exists(memoire_dir):
        os.makedirs(memoire_dir)
    
    # Check if the memoire file exists
    if os.path.exists(memoire_file):
        with open(memoire_file, "r") as f:
            return ast.literal_eval(f.read())
    
    task = list()
    duration = list()
    constrains = list()
    table = [task, duration, constrains]

    task.append('0')  # Alpha
    duration.append('0')  # Alpha
    constrains.append([])  # Alpha

    with open(constrain_table, "r") as f:
        lines = f.readlines()
        for line in lines:
            parts = line.split()
            task.append(parts[0])  # Tâche
            duration.append(parts[1])  # Durée
            # Lire les prédécesseurs correctement
            constraint = parts[2:] if len(parts) > 2 else []
            if not constraint:
                constraint = ['0']
            constrains.append(constraint)

    task.append(str(len(lines) + 1))  # Omega
    duration.append('0')  # Omega
    # Omega
    omega_constraints = [t for t in task if t not in [item for sublist in constrains for item in sublist] and t not in ['0', str(len(lines) + 1)]]
    constrains.append(omega_constraints)

    # Save the table to the memoire file
    with open(memoire_file, "w") as f:
        f.write(str(table))
    
    return table


def get_successors(tasks, constraints):
    # Retourne un dictionnaire des successeurs de chaque tâche
    successors = {task: [] for task in tasks}

    for i, task in enumerate(tasks):  
        for constrained_task in constraints[i]:  # Chaque tâche dont i dépend
            if constrained_task in tasks:
                successors[constrained_task].append(task)

    return successors

def get_predecessors(tasks, constraints):
    # Retourne un dictionnaire des prédécesseurs de chaque tâche
    predecessors = {task: [] for task in tasks}

    for i, task in enumerate(tasks):  
        for constrained_task in constraints[i]:  # Chaque tâche dont i dépend
            if constrained_task in tasks:
                predecessors[task].append(constrained_task)

    return predecessors

def has_no_cycles(graph):
    # Vérifie s'il y a des cycles dans le graphe
    def visit(node):
        if node in temp_mark:
            return False  # Cycle détecté
        if node not in perm_mark:
            temp_mark.add(node)
            for successor in graph.get(node, []):  # Vérifie les successeurs
                if not visit(successor):
                    return False
            temp_mark.remove(node)
            perm_mark.add(node)
        return True

    temp_mark = set()
    perm_mark = set()
    for node in graph:
        if node not in perm_mark:
            if not visit(node):
                return False
    return True

def has_no_negative_arcs(graph):
    # Vérifie s'il y a des arcs à valeur négative dans le graphe
    for row in graph:
        for value in row:
            if isinstance(value, int) and value < 0:  # Vérifie uniquement les entiers
                return False
    return True
    


def earliest_dates(tasks, durations, constraints):
    earliest = {task: 0 for task in tasks}  # Initialisation des dates au plus tôt
    
    for i, task in enumerate(tasks):
        for pred in constraints[i]:
            if pred in tasks:
                pred_index = tasks.index(pred)  # Trouver l'index de la tâche prédécesseur
                earliest[task] = max(earliest[task], earliest[pred] + int(durations[pred_index]))
    
    return earliest

def latest_dates(tasks, durations, constraints, project_end):
    latest = {task: project_end for task in tasks}  # Initialisation des dates au plus tard
    
    for task in reversed(tasks):
        successors = [t for t, preds in zip(tasks, constraints) if task in preds]
        if successors:
            latest[task] = min(latest[t] - int(durations[tasks.index(task)]) for t in successors)
    
    return latest

def compute_margins(earliest, latest):
    return {task: latest[task] - earliest[task] for task in earliest}

def critical_paths(margins):
    return [task for task, margin in margins.items() if margin == 0]
def analyze_schedule(constrain_table, trace_content):
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
    
    # Ajouter les résultats à la trace
    trace_content += "\nAnalyse de l'ordonnancement :\n"
    trace_content += tabulate(schedule_data, headers=headers, tablefmt="grid") + "\n"
    
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
    
    # Ajouter les chemins critiques à la trace
    trace_content += "\nChemins critiques :\n"
    for path in critical_paths_list:
        trace_content += " -> ".join(path) + "\n"
    
    return earliest, latest, margins, critical_paths_list, ranks, trace_content

def create_execution_trace(constrain_table, trace_content):

    trace_dir = "trace"
    if not os.path.exists(trace_dir):
        os.makedirs(trace_dir)

    # Nom du fichier de trace basé sur le fichier d'entrée
    base_name = os.path.basename(constrain_table)
    trace_file = os.path.join(trace_dir, f"trace_{base_name}")

    # Ajouter un horodatage au début de la trace
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    trace_header = f"Trace d'exécution - {timestamp}\n"
    trace_header += "=" * 50 + "\n"

    # Écrire la trace dans le fichier
    with open(trace_file, "w", encoding="utf-8") as f:
        f.write(trace_header)
        f.write(trace_content)

    # Afficher la trace dans la console
    print(trace_header + trace_content)

    print(f"\nTrace d'exécution enregistrée dans : {trace_file}")

def display_graph(constrain_table):
    trace_content = ""  # Variable pour stocker la trace
    table = constrain_table_reader(constrain_table)
    tasks, durations, constraints = table
    N = len(tasks)  # Nombre de tâches
    graph = np.full((N + 2, N + 2), '*', dtype=object)  # Matrice de valeurs initialisée

    # Remplir la matrice du graphe
    for i, task in enumerate(tasks):
        for constrained_task in constraints[i]:  # Chaque tâche dont i dépend
            if constrained_task in tasks:
                constrained_index = tasks.index(constrained_task)  # Trouver son index
                graph[i, constrained_index] = int(durations[constrained_index])  # Associer la bonne durée

    # Transposer la matrice pour inverser les colonnes et les lignes
    graph = graph.T

    # Création des en-têtes
    headers = ['0'] + [chr(65 + i) for i in range(N - 2)] + [str(N - 1)]

    # Affichage des en-têtes avec alignement
    trace_content += "    " + " ".join(f"{h:>3}" for h in headers) + "\n"
    for i in range(N):
        row = []
        for j in range(N):
            row.append(f"{graph[i, j]:>3}")
        trace_content += f"{headers[i]:>3} " + " ".join(row) + "\n"

    # Ajouter les successeurs et prédécesseurs à la trace
    successors = get_successors(tasks, constraints)
    predecessors = get_predecessors(tasks, constraints)

    # Vérification des propriétés du graphe
    graph_dict = {task: successors[task] for task in tasks}
    if has_no_cycles(graph_dict) and has_no_negative_arcs(graph):
        trace_content += "\nLe graphe ne contient pas de cycles.\n"
        trace_content += "Le graphe ne contient pas d'arcs à valeur négative.\n"
        trace_content += "-> C'est un graphe d'ordonnancement\n"
        _, _, _, _, _, trace_content = analyze_schedule(constrain_table, trace_content)
    else:
        if not has_no_cycles(graph_dict):
            trace_content += "\nLe graphe contient des cycles.\n"
        else:
            trace_content += "Le graphe ne contient pas de cycles.\n"
        if not has_no_negative_arcs(graph):
            trace_content += "Le graphe contient des arcs à valeur négative.\n"
        else:
            trace_content += "Le graphe ne contient pas d'arcs à valeur négative.\n"
        trace_content += "-> Ce n'est pas un graphe d'ordonnancement\n"

    # Enregistrer la trace
    create_execution_trace(constrain_table, trace_content)

    return graph

# Import de la table test pour création du fichier mémoire test
constrain_table = "contraintes/table 10.txt"
constrain_table_reader(constrain_table)

# Display graphe table test en mémoire
print("Graph matrix:")
display_graph("memoire/table 10.txt")