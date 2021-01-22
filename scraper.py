#!/usr/bin/env python
# -*- coding: utf8 -*-

from lxml import html
from random import randint
import requests
import json
import os

class Scraper:
    def __init__(self, region='en_US'):
        '''
        Since League of Legends is developed by Riot Games
        This program obtains its data from Riot Games services.
        '''
        self.base_url       = 'https://ddragon.leagueoflegends.com'

        try:
            # Verify the region
            if region in self.get_region():
                self.region     = region
            else:
                self.region     = 'en_US'


            # Get the data online
            self.patch                  = self.get_patch()
            self.champions_json         = self.get_champions_json()
            self.items_json             = self.get_items_json()
            self.summoner_spells_json   = self.get_summoner_spells_json()
            self.runes_json             = self.get_runes_json()

            # Read the data
            self.champions              = self.load_champions()
            self.items                  = self.items_json['data']
            self.positions              = ['Top', 'Jungle', 'Middle', 'Bottom (ADC/APC)', 'Support']
            self.summoner_spells        = self.load_summoner_spells()
            self.runes                  = self.load_runes()
            self.boots                  = self.load_boots()
            self.mythics                = self.load_mythics()
            self.legendary              = self.load_legendary()
        except:
            raise ValueError('Unable to load data!')

        self.images_url = f'{self.base_url}/cdn/{self.patch}/img'    # /item/1001.png

    def get_json_from_url(self, url):
        return requests.get(f'{self.base_url}/{url}.json').json()

    def download_image(self, url, image_name, directory='resources'):
        response = requests.get(url)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(f'{directory}/{image_name}', "wb") as f:                               # wb mode to open in write-and-binary mode
            f.write(response.content)
            f.close()

    def get_region(self):
        return self.get_json_from_url('cdn/languages')

    def get_patch(self):
        return self.get_json_from_url('api/versions')[0]

    def get_champions_json(self):
        return self.get_json_from_url(f'cdn/{self.patch}/data/{self.region}/champion')

    def get_items_json(self):
        return self.get_json_from_url(f'cdn/{self.patch}/data/{self.region}/item')

    def get_summoner_spells_json(self):
        return self.get_json_from_url(f'cdn/{self.patch}/data/{self.region}/summoner')

    def get_runes_json(self):
        return self.get_json_from_url(f'cdn/{self.patch}/data/{self.region}/runesReforged')

    def load_champions(self):
        champions = [champion for champion in self.champions_json['data']]
        for i, n in enumerate(champions[74:]):
            if n == 'MonkeyKing': champions[74 + i] = 'Wukong'
        return champions

    def load_summoner_spells(self):
        return [
            self.summoner_spells_json['data'][e]['name']
            for e in self.summoner_spells_json['data'] if 'CLASSIC' in self.summoner_spells_json['data'][e]['modes']
        ]

    def load_boots(self):
        return [
            e for e in self.items
            if 'Boots' in self.items[e]['tags']
            and not 'into' in self.items[e]
            and self.items[e]['maps']['11']
        ]

    def load_mythics(self):
        return [
            e for e in self.items
            if 'rarityMythic' in self.items[e]['description']
            and not e in self.boots
            and self.items[e]['maps']['11']
        ]

    def load_legendary(self):
        return [
            e for e in self.items
            if not 'rarityMythic' in self.items[e]['description']
            and not 'into' in self.items[e]
            and self.items[e]['gold']['base'] > 500
            and not e in self.boots
            and self.items[e]['maps']['11']
        ]

    def load_runes(self):
        return [
            [
                [
                    self.runes_json[i]['slots'][j]['runes'][k]['key']
                    for k in range(len(self.runes_json[i]['slots'][j]['runes']))
                ]
                for j in range(len(self.runes_json[i]['slots']))
            ]
            for i in range(len(self.runes_json))
        ]

    def generate_pick(self):
        # Champion <Aatrox:...:Zyra>
        champion = self.champions[randint(0, len(self.champions) - 1)]

        # Position <top:jungle:mid:adc:support>
        position = self.positions[randint(0, len(self.positions) - 1)]
        mythic = self.items[self.mythics[randint(
            0, len(self.mythics) - 1)]]['name']

        # Runes <Electrocute:...:Aery>
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

        # Spells <Q:W:E>
        spells = 'QWE'[randint(0, 2)]
        for _ in range(2):
            l = 'QWE'[randint(0, 2)]
            while l in spells:
                l = 'QWE'[randint(0, 2)]
            spells += l

        # Summoner spells
        if position == 'Jungle':
            summoner_spells = [self.summoner_spells[randint(0, len(self.summoner_spells) - 1)], 'Smite']
        else:
            summoner_spells = [self.summoner_spells[randint(0, len(self.summoner_spells) - 1)] for _ in range(2)]
        while summoner_spells[0] == summoner_spells[1]:
            summoner_spells[1] = self.summoner_spells[randint(0, len(self.summoner_spells) - 1)]

        # Legendary items
        legendaries = [self.items[self.legendary[randint(0, len(self.legendary) - 1)]]['name']]
        while len(legendaries) < 4:
            new_item = self.items[self.legendary[randint(0, len(self.legendary) - 1)]]['name']
            if new_item not in legendaries:
                legendaries.append(new_item)

        # Boots
        if champion == 'Cassiopeia':
            while len(legendaries) < 5:
                new_item = self.items[self.legendary[randint(0, len(self.legendary) - 1)]]['name']
                if new_item not in legendaries:
                    legendaries.append(new_item)
        else:
            boots = self.items[self.boots[randint(0, len(self.boots) - 1)]]['name']

        return [
            champion, position, mythic, legendaries, summoner_spells, spells, runes
        ] if champion == 'Cassiopeia' else [
            champion, position, mythic, legendaries, summoner_spells, spells, runes, boots
        ]
