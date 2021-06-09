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
combination_best = 0
bonus_global = 0
bonus_best = 0
actions_max = 0
count_combinations = 0

actions = import_csv("data/actions.csv")


def find_action(this_action):
    # find a specific action in the action list
    global actions
    for element in actions:
        if element["action"] == this_action:
            return element
    return None


def total_combination(this_combination):
    # calculate the total result of a set of actions (cost + bonus)
    global budget_max
    cost = 0
    for this_action in this_combination:
        cost += int(find_action(this_action)["price"])
        if cost > budget_max:
            return None
    return cost


def bonus_combination(this_combination):
    # calculate the bonus of an actions set
    bonus = 0
    for this_action in this_combination:
        bonus += int(find_action(this_action)["price"]) * (
                int(find_action(this_action)["percentile"]) / 100
        )
    return bonus


for action in actions:
    actions_list.append(action["action"])

for action in actions:
    prices_list.append(action["price"])

# Find the cheapest action to determinate the maximum number of action
# that can be buy
prices_list.sort()

budget = 0
elements = 0

for el in prices_list:
    budget += int(prices_list[elements])
    if budget < budget_max:
        elements += 1
    else:
        break

actions_max = elements

print(f"Il y a {actions_max} éléments maximum.")

print(f"Action list: {actions_list}")
for combination_length in range(1, actions_max):
    combination = permutations(actions_list, combination_length)
    for el in combination:
        count_combinations += 1
        if total_combination(el):
            bonus_global = total_combination(el) + bonus_combination(el)
            if bonus_global > bonus_best:
                combination_best = list(el)
                bonus_best = total_combination(
                    combination_best
                ) + bonus_combination(combination_best)
                print(
                    f"--- Combinaison {count_combinations} ---\n{el}\n"
                    f"Est à notre portée pour un coût de "
                    f"{total_combination(combination_best)} "
                    f"et un bénéfice de {bonus_combination(combination_best)}"
                )
