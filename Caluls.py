import os
import ast
import numpy as np
from tabulate import tabulate
from Display import* 
from Table import* 

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
