#!/bin/bash venv python3
import csv
from itertools import permutations

budget_max = 500  # Budget maximum
actions_dict = {}
actions_dict_percentile = {}
actions_list = []
prices_list = []
process_list = []
combination_best = 0
bonus_global = 0
bonus_best = 0
actions_max = 0
count_combinations = 0


def import_csv(filename):
    # Import a CSV, return a table
    every_action = []
    with open(filename, encoding="utf-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile, quotechar="%")
        for row in reader:
            every_action.append(row)
    return every_action


def total_combination(this_combination):
    # calculate the total result of a set of actions (cost + bonus)
    # big_O = 1
    global budget_max
    cost = 0
    for this_action in this_combination:
        cost += int(actions_dict[this_action])
        if cost > budget_max:
            return None
    return cost


def bonus_combination(this_combination):
    # calculate the bonus of an actions set
    # big_O = 1 + len(this_combination)
    bonus = 0
    for this_action in this_combination:
        bonus += int(actions_dict[this_action]) * (
            int(actions_dict_percentile[this_action]) / 100
        )
    return bonus


actions = import_csv("data/actions.csv")

for action in actions:
    actions_list.append(action["action"])
    actions_dict[action["action"]] = int(action["price"])
    actions_dict_percentile[action["action"]] = int(action["percentile"])

for action in actions:
    prices_list.append(action["price"])

# Find the cheapest actions to determinate the maximum number of action
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

actions_max = elements + 1
# From this point big_O = 159

# Here is the heart of bruteforce, trying every combination
for combination_length in range(1, actions_max):
    combination = permutations(actions_list, combination_length)
    print(f"New range: {combination_length} / {actions_max}")
    for el in combination:
        count_combinations += 1
        if total_combination(el):
            bonus_global = bonus_combination(el)
            if bonus_global > bonus_best:
                combination_best = list(el)
                bonus_best = bonus_global
                print(
                    f"--- Combination {count_combinations} ---\n{el}\n"
                    f"Can be buy for "
                    f"{total_combination(combination_best)} "
                    f"and generate a bonus of "
                    f"{bonus_combination(combination_best)}"
                )
# Total big_O = 243_290_200_000_000_000_159 (Maximum big_O for 20 actions)
# big_O = len(actions_list) + 161 + exp(len(actions)) (is exponential)
