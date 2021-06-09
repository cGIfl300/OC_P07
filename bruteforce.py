#!/bin/bash venv python3
import csv
from itertools import permutations


def import_csv(filename):
    # Import a CSV, return a table
    every_action = []
    with open(filename, encoding="utf-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile, quotechar="%")
        for row in reader:
            every_action.append(row)
    return every_action


budget_max = 500  # Budget maximum
actions_list = []
prices_list = []
combinaison_gagnante = 0
retour_global = 0
retour_gagnante = 0
maximum_actions = 0
compteur_combinaisons = 0

actions = import_csv("data/actions.csv")


def found_action(action):
    # found a specific action in the action list
    global actions
    for element in actions:
        if element["action"] == action:
            return element
    return None


def cout_portefeuille(portefeuille):
    # calculate the total result of a set of actions (cost + bonus)
    global budget_max
    cout = 0
    for action in portefeuille:
        cout += int(found_action(action)["price"])
        if cout > budget_max:
            return None
    return cout


def bonus_portefeuille(portefeuille):
    # calculate the bonus of an actions set
    bonus = 0
    for action in portefeuille:
        bonus += int(found_action(action)["price"]) * (
            int(found_action(action)["percentile"]) / 100
        )
    return bonus


for action in actions:
    actions_list.append(action["action"])

for action in actions:
    prices_list.append(action["price"])


# Find the cheapest action to determinate the maximum number of action that can be buy
prices_list.sort()

budget = 0
elements = 0
for el in prices_list:
    budget += int(prices_list[elements])
    if budget < budget_max:
        elements += 1
    else:
        break

maximum_actions = elements

print(f"Il y a {maximum_actions} éléments maximum.")

print(f"Action list: {actions_list}")
for nombre_dactions in range(1, maximum_actions):
    combi = permutations(actions_list, nombre_dactions)
    for el in combi:
        compteur_combinaisons += 1
        if cout_portefeuille(el):
            retour_global = cout_portefeuille(el) + bonus_portefeuille(el)
            if retour_global > retour_gagnante:
                combinaison_gagnante = list(el)
                retour_gagnante = cout_portefeuille(
                    combinaison_gagnante
                ) + bonus_portefeuille(combinaison_gagnante)
                print(
                    f"""--- Combinaison {compteur_combinaisons} ---\n{el}
Est à notre portée pour un coût de {cout_portefeuille(combinaison_gagnante)} et un bénéfice de {bonus_portefeuille(combinaison_gagnante)}"""
                )
