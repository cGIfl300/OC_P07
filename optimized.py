#!/bin/bash venv python3
import csv
from operator import itemgetter

budget = 500  # Budget maximum
actions_list = []
optimized_list = []
process_list = []
combination = []
total_return = 0
actual_value = 0
jackpot = False  # Exit from the loop


def import_csv(filename):
    # Import a CSV, return a table
    every_action = []
    with open(filename, encoding="utf-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile, quotechar="%")
        for row in reader:
            every_action.append(row)
    return every_action


actions = import_csv("data/dataset1.csv")
# actions = import_csv("data/dataset2.csv") # Big_O = Nombre d'actions dans la base de données (1000)

for i in actions:
    i["percentile"] = float(i["percentile"]) # Big_O = Nombre d'actions dans la base de données (1000)

optimized_list = sorted(actions, key=itemgetter("percentile"))

while not jackpot:
    actual_value = optimized_list.pop()
    if budget - float(actual_value["price"]) < 0:
        jackpot = True
    else:
        budget -= float(actual_value["price"])
        total_return += (
            float(actual_value["price"]) * actual_value["percentile"] / 100
        )
        combination.append(actual_value)

print(
    f"Décision : {combination}\nPour un montant de {500 - budget} et un"
    f" retour de {total_return}"
)

# Big_O:
# N = Nombre d'actions dans la base de données (1000)
# ** le nombre maximum d'actions achetables corresponds à l'intégralité du catalogue
# 5 * N
# Pour 1000 actions: 5000