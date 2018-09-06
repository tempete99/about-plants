#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from yattag import Doc

# DOTO:
# - URLs/LINKS
#    Every family has a directory where their spp pages are stored
# - HTML
#    Families have their own webpages with a list of spp
# - Put all generated website in a different directory 'website/'

class Family(object):
    def __init__(self, name):
        self.name = name
        self.url = self.name + '.html'
        # Will store species
        self.spp = []

#     def __repr__(self, name):
#         return self.name
#     def __str__(self, name):
#         return self.name

class Plant(object):
    def __init__(self, fr, lat, fam, desc, tags):
        self.french_name = fr
        self.latin_name = lat
        self.family = fam
        self.description = desc
        self.tags = tags
        # Set tags to none if empty string
        if self.tags.strip() == '':
            self.tags = None
        else:
            # At this point tags are still strings
            # Remove spaces. No need for strip()
            self.tags = self.tags.replace(' ', '')
            # Remove last comma if there is one
            if self.tags[-1] == ',':
                self.tags = self.tags[:-1]
            # Make tags a list
            self.tags = self.tags.split(',')
        # Generate per-plant page url suffix. Deal with   -Spaces-      -Dots (ssp.)-
        self.url = 'plantlist/' + self.latin_name.replace(' ', '_').replace('.', '') + '.html'


families = []

with open('plants.csv', 'r') as f:
    lists = csv.reader(f)
    for row in lists:
        family = row[2].split(" ")[0]
        # Create family if not already created
        if family not in [f.name for f in families]:
            families.append(Family(family))
        for i in families:
            if i.name == family:
                families[families.index(i)].spp.append(Plant(row[0],
                                                           row[1],
                                                           row[2],
                                                           row[3],
                                                           row[4],))
# Sorting families alphabetically
families.sort(key=lambda x: x.name)
# Sorting spp inside families alphabetically
for f in families:
    f.spp.sort(key=lambda x: x.latin_name)
    
# Create a list containing aliases of every spp
# allspp = sorted([s for s in [f.spp for f in families]]) # Does not work
allspp = []
for f in families:
    for s in f.spp:
        allspp.append(s)
allspp.sort(key=lambda x: x.latin_name)

# def createpage():
#     doc, tag, text, line = Doc().ttl()
#     doc.asis("<!DOCTYPE html>")
#     with tag('html'):
#         with tag('head'):
#             line('title', 'Bonsoir')
#             doc.asis('<meta charset="utf-8">') # Important
#         
#         with tag('body'):
#             line('h1', 'Bienvenue sur mon petit site de merde')
#             with tag('ul'):
#                 for i in plants:
#                     plant = plants[i]
#                     with tag('li'):
#                         doc.asis('<em>%s</em> - %s ' %(plant.latin_name,
#                                                       plant.french_name))
#                         # Hyperlink to per-plant page
#                         with tag('a', href=plant.url):
#                             doc.stag('img', src='img/freccia.png')
# 
#             with tag('div'):
#                 with tag('p'):
#                     line('h2', 'Voici une liste des familles:') 
#                     with tag('ul'):
#                         for family in sortedfamilies:
#                             line('li', families[family].name)
#                             with tag('ul'):
#                                 for i in families[family].spp:
#                                     line('li', i)
# 
#     return doc.getvalue()
# 
# 
# with open("index.html", "w") as f:
#     f.write(createpage())
# 
# 
# # Function to generate per-plant pages
# def plantpage(plantobject):
#     doc, tag, text, line = Doc().ttl()
#     doc.asis("<!DOCTYPE html>")
#     with tag('html'):
#         with tag('head'):
#             line('title', plantobject.latin_name)
#             doc.asis('<meta charset="utf-8">') # Important
# 
#         with tag('body'):
#             line('h1', plantobject.latin_name)
#             line('h2', plantobject.french_name)
#             line('h3', plantobject.family)
#             with tag('p'):
#                 text(plantobject.description)
#             if plantobject.tags:
#                 with tag('ul'): 
#                     for planttag in plantobject.tags:
#                         line('li', planttag)
# 
#     return doc.getvalue()
# 
# # Write all per-plant pages
# for i in plants:
#     plant = plants[i]
#     with open(plant.url, 'w') as file:
#         file.write(plantpage(plant))
