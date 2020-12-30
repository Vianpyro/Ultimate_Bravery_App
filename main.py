#!/usr/bin/env python
# -*- coding: utf8 -*-
from lxml import html
from random import randint
import requests, json

class Scraper:
    def __init__(self):
        '''
        Since League of Legends is developed by Riot Games
        This program obtains its data from Riot Games services.
        '''
        self.base_url               = 'https://ddragon.leagueoflegends.com'
        self.patch                  = requests.get(f'{self.base_url}/api/versions.json').json()[0]
        self.champions_json         = requests.get(f'{self.base_url}/cdn/{self.patch}/data/en_US/champion.json').json()
        self.items_json             = requests.get(f'{self.base_url}/cdn/{self.patch}/data/en_US/item.json').json()
        self.summoner_spells_json   = requests.get(f'{self.base_url}/cdn/{self.patch}/data/en_US/summoner.json').json()
        self.runes_json             = requests.get(f'{self.base_url}/cdn/{self.patch}/data/en_US/runesReforged.json').json()

        self.champions              = [champion for champion in self.champions_json['data']]
        self.items                  = self.items_json['data']
        self.positions              = ['Top', 'Jungle', 'Middle', 'Bottom (ADC/APC)', 'Support']
        self.summoner_spells        = [self.summoner_spells_json['data'][e]['name'] for e in self.summoner_spells_json['data'] if 'CLASSIC' in self.summoner_spells_json['data'][e]['modes']]
        self.runes = [
            [
                [
                    self.runes_json[i]['slots'][j]['runes'][k]['key']
                    for k in range(len(self.runes_json[i]['slots'][j]['runes']))
                ]
                for j in range(len(self.runes_json[i]['slots']))
            ]
            for i in range(len(self.runes_json))
        ]
        self.boots                  = [
            e for e in self.items
            if 'Boots' in self.items[e]['tags']
            and not 'into' in self.items[e]
            and self.items[e]['maps']['11']
        ]
        self.mythics        = [
            e for e in self.items
            if 'rarityMythic' in self.items[e]['description']
            and not e in self.boots
            and self.items[e]['maps']['11']
        ]
        self.legendary      = [
            e for e in self.items
            if not 'rarityMythic' in self.items[e]['description']
            and not 'into' in self.items[e]
            and self.items[e]['gold']['base'] > 500
            and not e in self.boots
            and self.items[e]['maps']['11']
        ]

        print(self)

    def generate_pick(self):
        champion    = self.champions[randint(0, len(self.champions) - 1)]
        position    = self.positions[randint(0, len(self.positions) - 1)]
        mythic      = self.items[self.mythics[randint(0, len(self.mythics) - 1)]]['name']

        main_branch = randint(0, len(self.runes) - 1)
        secondary_branch = randint(0, len(self.runes) - 1)
        while secondary_branch == main_branch:
            secondary_branch = randint(0, len(self.runes) - 1)

        runes = [
            [
                self.runes[main_branch][i][randint(
                    0, len(self.runes[main_branch][i]) - 1)]
                for i in range(4)
            ],
            [
                self.runes[secondary_branch][j][randint(
                    0, len(self.runes[secondary_branch][j]) - 1)]
                for j in range(1, 3)
            ]
        ]

        spells      = 'QWE'[randint(0, 2)]
        for _ in range(2):
            l = 'QWE'[randint(0, 2)]
            while l in spells: l = 'QWE'[randint(0, 2)]
            spells += l

        if position == 'Jungle':
            summoner_spells = [self.summoner_spells[randint(0, len(self.summoner_spells) - 1)], 'Smite']
        else:
            summoner_spells = [self.summoner_spells[randint(0, len(self.summoner_spells) - 1)] for _ in range(2)]

        if champion == 'Cassiopeia':
            legendaries = [self.items[self.legendary[randint(0, len(self.legendary) - 1)]]['name'] for _ in range(6)]
        else:
            legendaries = [self.items[self.legendary[randint(0, len(self.legendary) - 1)]]['name'] for _ in range(5)]
            boots       = self.items[self.boots[randint(0, len(self.boots) - 1)]]['name']

        r = f"""
        CHAMPION:\t{champion}
        POSITION:\t{position}
        MYTHIC:\t\t{mythic}
        LEGENDARY:\t{legendaries}
        SUMMONERS:\t{summoner_spells[0]}, {summoner_spells[1]}
        SPELLS:\t\t{spells[0]} > {spells[1]} > {spells[2]}
        RUNES:\t\t{runes}
        """

        if champion != 'Cassiopeia': r += f'BOOTS:\t\t{boots}\n'
        return r

    def __str__(self):
        return self.generate_pick()

pick = Scraper()
while input("Re-roll? [y/n]: ")[0].lower() == 'y':
    print(pick)