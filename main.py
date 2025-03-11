import math

def constrain_table_reader(constrain_table):
    task = list()
    duration = list()
    constrains = list()
    table = [task, duration, constrains]
    with open(constrain_table, "r") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            task.append(lines[i].split()[0])
        for i in range(len(lines)):
            duration.append(lines[i].split()[1])
        for i in range(len(lines)):
            constrains.append(lines[i].split()[2:])
    return table

#Import de la table C01 de la feuille de TD pour test
tabletest = constrain_table_reader("contraintes/tabletest.txt")
print(tabletest)