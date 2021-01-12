#!/usr/bin/env python
# -*- coding: utf8 -*-

import re
import tkinter as tk
from scraper import Scraper

window = tk.Tk()
window.title("Ultimate Bravery")
window.geometry("365x325")
pick = Scraper()


def putSpace(string):
    return ' '.join(re.findall('[A-Z][a-z]*', string))

######################
# ANSWER PULL
######################
def random_display():
    result = pick.generate_pick()
    print(result)
    results_display = tk.Text(master=window, height=18, width=45)
    results_display.grid(column=0, row=3)

    # Role
    results_display.insert(tk.END, f'Champion:\t\t{putSpace(result[0])}\n')
    results_display.insert(tk.END, f'Lane:\t\t{result[1]}\n')

    # Runes
    results_display.insert(tk.END, f'Runes:\n')
    for rune in result[6][0]:
        results_display.insert(tk.END, f'\t\t- {putSpace(rune)}\n')
    results_display.insert(tk.END, f'\t\t+ {putSpace(result[6][1][0])}\n\t\t+ {putSpace(result[6][1][1])}\n')

    # Spells
    results_display.insert(tk.END, f'Summoner spells:\t{result[4][0]} & {result[4][1]}\n')
    results_display.insert(tk.END, f'Spells order:\t\t{result[5][0]} > {result[5][1]} > {result[5][2]}\n')

    # Items
    results_display.insert(tk.END, f'Items:\n\t\t+ {result[2]}\n')
    for item in result[3]:
        results_display.insert(tk.END, f'\t\t- {item}\n')

    # Boots
    if len(result[3]) == 4:
        results_display.insert(tk.END, f'Boots:\t\t{result[7]}')

######################
# BUTTON
######################
button = tk.Button(text="Good Luck!", command=random_display)
button.grid(column=0, row=1)
random_display()
window.mainloop()
