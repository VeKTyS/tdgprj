import os
import ast
import numpy as np
from tabulate import tabulate
from Display import* 
from Caluls import* 

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