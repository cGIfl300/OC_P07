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


actions = import_csv("data/actions.csv")
for i in actions:
    i["percentile"] = int(i["percentile"])
optimized_list = sorted(actions, key=itemgetter("percentile"), reverse=True)
print(optimized_list)

while not jackpot:
    actual_value = optimized_list.pop()
    if budget - int(actual_value["price"]) < 0:
        jackpot = True
    else:
        budget -= int(actual_value["price"])
        total_return += (
            int(actual_value["price"]) * actual_value["percentile"] / 100
        )
        combination.append(actual_value)

print(
    f"Décision : {combination}\nPour un montant de {500 - budget} et un"
    f" retour de {total_return}"
)
