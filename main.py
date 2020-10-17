#!/usr/bin/env python
# -*- coding: utf8 -*-
from random import randint
from data import *

champion = CHAMPIONS[randint(0, len(CHAMPIONS) - 1)]
role = ROLES[randint(0, len(ROLES) - 1)]
boots = BOOTS[randint(0, len(BOOTS) - 1)]
spells = ['QWE'[randint(0, 2)]]

#################################
#   RUNES
#################################

runes_pages = [path for path in RUNES[0]]
pre_runes = [randint(0, len(runes_pages) - 1) for _ in range(2)]
while pre_runes[0] == pre_runes[1]:
    pre_runes[1] = randint(0, len(runes_pages) - 1)

runes_paths = [
    RUNES[0][runes_pages[pre_runes[0]]],
    RUNES[0][runes_pages[pre_runes[1]]]
]

runes = [
    [
        [runes_paths[0][i][randint(0, len(runes_paths[0][i]) - 1)] for i in range(4)],
        [runes_paths[1][j + 1 + (pre_runes[0] + pre_runes[1]) // 4]
            [randint(0, len(runes_paths[1][j + 1 + (pre_runes[0] + pre_runes[1]) // 4]) - 1)] for j in range(2)]
    ],
    [RUNES[1][f"Slot{slot + 1}"][randint(0, 2)] for slot in range(3)]
]

#################################
#   BUILD
#################################

len_finished_items = len(FINISHED_ITEMS)

if role == "Support": build = [SUPPORT_ITEMS[randint(0, len(SUPPORT_ITEMS) - 1)]]
elif role == "Jungle":
    core_items = ["Skirmisher's Sabre", "Stalker's Blade"]
    enchant_items = ["Bloodrazor", "Cinderhulk", "Runic Echoes", "Warrior"]
    build = [f"{core_items[randint(0, len(core_items) - 1)]} ({enchant_items[randint(0, len(enchant_items) - 1)]})"]
else:
    build = [FINISHED_ITEMS[randint(0, len_finished_items - 1)]]

while len(build) < 5:
    new_item = FINISHED_ITEMS[randint(0, len_finished_items - 1)]
    if not new_item in build:
        build.append(new_item)

#################################
#   SUMMONER SPELLS
#################################

len_summoner_spells = len(SUMMONER_SPELLS)

if role == "Jungle":
    sums = ["Smite"]
else: sums = [SUMMONER_SPELLS[randint(0, len_summoner_spells - 1)]]

while len(sums) < 2:
    new_sums = SUMMONER_SPELLS[randint(0, len_summoner_spells - 1)]
    if not new_sums in sums:
        sums.append(new_sums)

#################################
#   SPELLS ORDER
#################################

while len(spells) < 3:
    new_spell = 'QWE'[randint(0, 2)]
    if not new_spell in spells:
        spells.append(new_spell)

#################################
#   DISPLAY
#################################

print(f"""
ROLE: {role}
CHAMPION: {champion}
SUMMONERS: {sums[0]}, {sums[1]}
RUNES: ({runes_pages[pre_runes[0]]}, {runes_pages[pre_runes[1]]})
\t- {runes[0][0][0]} : {runes[0][0][1]} - {runes[0][0][2]} - {runes[0][0][3]}
\t- {runes[0][1][0]} - {runes[0][1][1]}
\t- {runes[1][0]} - {runes[1][1]} - {runes[1][2]}

SPELLS: {spells[0]} > {spells[1]} > {spells[2]}
BUILD: {build}
BOOTS: {boots}
""")

input("Good luck, have fun !")
