#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from yattag import Doc

# On commencera par creer toutes les familles au fur et a mesure
# Que les spp defilent, en ajoutant ces derniers petit a petit aux
# listes .spp des familles
# On triera ensuite cette liste avec spp.sort(key=lambda x: x.latin_name)
# On rangera les objects 

class Family(object):
    def __init__(self, name):
        self.name = name
        self.url = self.name + '.html'
        # Will store species
        self.spp = []

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

# Create a dictionnary with all plant-objects
plants = {}
with open('plants.csv', 'r') as f:
    lists = csv.reader(f)
    for row in lists:
        # Object name is latin name
        objectname = row[1]
        # Create the object
        plants[objectname] = Plant( row[0], row[1], row[2], row[3], row[4] )




families = {}
for i in plants:
    plant = plants[i]
    # Stick to the the first family word. Filter old family names, synonyms
    # or any non-phylogenetic classification.
    family = plant.family.split(" ")[0]
    if family not in families:
        families[family] = Family(family)
    families[family].spp.append(plant.latin_name)
# Sort species in families
for family in families:
    families[family].spp.sort()
# Create a sorted list of all existing families
sortedfamilies = sorted([x for x in families])

def createpage():
    doc, tag, text, line = Doc().ttl()
    doc.asis("<!DOCTYPE html>")
    with tag('html'):
        with tag('head'):
            line('title', 'Bonsoir')
            doc.asis('<meta charset="utf-8">') # Important
        
        with tag('body'):
            line('h1', 'Bienvenue sur mon petit site de merde')
            with tag('ul'):
                for i in plants:
                    plant = plants[i]
                    with tag('li'):
                        doc.asis('<em>%s</em> - %s ' %(plant.latin_name,
                                                      plant.french_name))
                        # Hyperlink to per-plant page
                        with tag('a', href=plant.url):
                            doc.stag('img', src='img/freccia.png')

            with tag('div'):
                with tag('p'):
                    line('h2', 'Voici une liste des familles:') 
                    with tag('ul'):
                        for family in sortedfamilies:
                            line('li', families[family].name)
                            with tag('ul'):
                                for i in families[family].spp:
                                    line('li', i)

    return doc.getvalue()


with open("index.html", "w") as f:
    f.write(createpage())


# Function to generate per-plant pages
def plantpage(plantobject):
    doc, tag, text, line = Doc().ttl()
    doc.asis("<!DOCTYPE html>")
    with tag('html'):
        with tag('head'):
            line('title', plantobject.latin_name)
            doc.asis('<meta charset="utf-8">') # Important

        with tag('body'):
            line('h1', plantobject.latin_name)
            line('h2', plantobject.french_name)
            line('h3', plantobject.family)
            with tag('p'):
                text(plantobject.description)
            if plantobject.tags:
                with tag('ul'): 
                    for planttag in plantobject.tags:
                        line('li', planttag)

    return doc.getvalue()

# Write all per-plant pages
for i in plants:
    plant = plants[i]
    with open(plant.url, 'w') as file:
        file.write(plantpage(plant))
