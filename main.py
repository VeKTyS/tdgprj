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

def display_graph(constrain_table):
    table = constrain_table_reader(constrain_table)
    tasks, durations, constraints = table
    N = len(tasks) # Nombre de tâches 
    graph = np.zeros((N + 2, N + 2), dtype=int)
    
    for i, task in enumerate(tasks):  
        for constrained_task in constraints[i]:  # Chaque tâche dont i dépend
            if constrained_task in tasks:
                constrained_index = tasks.index(constrained_task)  # Trouver son index
                graph[i, constrained_index] = int(durations[constrained_index])  # Associer la bonne durée
    
    # Ajout des nœuds fictifs 0 et N+1
    for i in range(1, N + 1):
        graph[i, 0] = 0
        graph[N + 1, i] = 0

    # Transpose the graph matrix
    graph = graph.T

    # Création des en-têtes
    #headers = ['0'] + [chr(65 + i) for i in range(N)] + [str(N + 1)]
    headers = ['0'] + [chr(65 + i) for i in range(N-2)] + [str(N-1)]

    # Affichage des en-têtes avec alignement
    print("    " + " ".join(f"{h:>3}" for h in headers))
    for i in range(N):
        row = []
        for j in range(N):
            if graph[i, j] == 0 and i != 0 and j != N + 1:
                row.append("  *")
            else:
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

    return graph

# Import de la table test pour création du fichier mémoire test
constrain_table = "contraintes/tabletest.txt"
constrain_table_reader(constrain_table)

# Display graphe table test en mémoire
print("Graph matrix:")
display_graph("memoire/tabletest.txt")
