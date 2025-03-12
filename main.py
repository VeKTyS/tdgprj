import os
import ast
import numpy as np

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

    task.append('0') # Alpha
    duration.append('0') # Alpha
    constrains.append([]) # Alpha

    with open(constrain_table, "r") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            task.append(lines[i].split()[0])
        for i in range(len(lines)):
            duration.append(lines[i].split()[1])
        for i in range(len(lines)):
            constraint = lines[i].split()[2:]
            if not constraint:
                constraint = ['0']
            constrains.append(constraint)

    task.append(str(len(lines) + 1)) # Omega
    duration.append('0') # Omega
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
            return False
        if node not in perm_mark:
            temp_mark.add(node)
            for successor in graph[node]:
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
            if isinstance(value, int) and value < 0:
                return False
    return True

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
    print("\nSuccesseurs des tâches :")
    for task, succ in successors.items():
        print(f"Tâche {task}: {', '.join(succ) if succ else 'Aucun successeur'}")    

    predecessors = get_predecessors(tasks, constraints)
    print("\nPrédécesseurs des tâches :")
    for task, pred in predecessors.items():
        print(f"Tâche {task}: {', '.join(pred) if pred else 'Aucun prédécesseur'}")

    # Vérification des propriétés du graphe
    graph_dict = {task: successors[task] for task in tasks}
    if has_no_cycles(graph_dict) and has_no_negative_arcs(graph):
        print("\nLe graphe ne contient pas de cycles.")
        print("Le graphe ne contient pas d'arcs à valeur négative.")
        print("-> C'est un graphe d'ordonnancement\n")
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

# Import de la table test pour création du fichier mémoire test
constrain_table = "contraintes/tabletest.txt"
constrain_table_reader(constrain_table)

# Display graphe table test en mémoire
print("Graph matrix:")
display_graph("memoire/tabletest.txt")