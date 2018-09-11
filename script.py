#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv
import posixpath
from urllib.parse import urlparse, urljoin, urlunparse
# Dependencies:
from yattag import Doc, indent

# Function to smartly handle relative urls. From:
# https://mensfeld.pl/2011/09/relative-and-absolute-urls-expanding-in-python/
def expand_url(home, url):
    join = urljoin(home,url)
    url2 = urlparse(join)
    path = posixpath.normpath(url2[2])
    return urlunparse((url2.scheme,url2.netloc,path,url2.params,url2.query,url2.fragment))


# Prefix directory for the whole website
prefix = 'website/'
try:
    os.mkdir(prefix)
except FileExistsError:
    pass


class Stylesheet(object):
    def __init__(self):
        self.filename = "style.css"
        self.content = ''
    def WriteStyleSheet(self):
        with open( prefix + self.filename, 'w') as file:
            file.write(self.content)

# Function to write html file with correct indentation
def writeyattag(file, doc):
    with open(file, 'w') as f:
        f.write(indent(doc.getvalue(), indent_text = True))

class Family(object):
    def __init__(self, name):
        self.name = name.split(" ")[0]
        self.url = self.name + '/index.html'
        # Will store species objects in a directory
        self.spp = []
    def SortSpp(self):
        # Sorting spp inside family
        self.spp.sort(key=lambda x: x.latin_name)
    def WriteFamilyIndexPage(self):
        doc, tag, text, line = Doc().ttl()
        doc.asis("<!DOCTYPE html>")
        with tag('html'):
            with tag('head'):
                line('title', self.name)
                doc.asis('<meta charset="utf-8">') # Important
                doc.asis('<link rel="stylesheet" href="%s">' % ('../' + stylesheet.filename))
        with tag('body'):
            with tag('body'):
                line('h1', self.name)
            with tag('ul'):
                for sp in self.spp:
                    with tag('li'):
                        with tag('a', href= sp.filename):
                            text(sp.latin_name)
        # Create family directory
        try:
            os.mkdir(prefix + expand_url(self.url, '.'))
        except FileExistsError:
            pass
        # Write page to disk
        writeyattag(prefix + self.url, doc)
        # with open(prefix + self.url, 'w') as file:
        #    file.write(doc.getvalue())


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
        # Generate per-plant page url.Deal with   -Spaces-      -Dots (ssp.)-
        self.filename = self.latin_name.replace(' ', '_').replace('.', '') + '.html'
        self.familyurl = self.family.split(' ')[0] + '/' # Must be equal in Family object
        self.url = self.familyurl + self.filename
    def WritePlantPage(self):
        doc, tag, text, line = Doc().ttl()
        doc.asis("<!DOCTYPE html>")
        with tag('html'):
            with tag('head'):
                line('title', self.latin_name)
                doc.asis('<meta charset="utf-8">') # Important
                doc.asis('<link rel="stylesheet" href="%s">' % ('../' + stylesheet.filename))
            with tag('body'):
                line('h1', self.latin_name)
                line('h2', self.french_name)
                # line('h3', self.family)
                with tag('h3'):
                    with tag('a', href= '../' + self.familyurl + 'index.html'):
                        text(self.family)
                with tag('p'):
                    text(self.description)
                if self.tags:
                    with tag('ul'): 
                        for planttag in self.tags:
                            line('li', planttag)
        # Write page to disk
        writeyattag(prefix + self.url, doc)
        #with open(prefix + self.url, 'w') as file:
        #    file.write(doc.getvalue())


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

# Sorting spp inside every family
for f in families:
    f.SortSpp()
    
# Create a list containing aliases of every spp sorted by Latin name
# allspp = sorted([s for s in [f.spp for f in families]]) # Does not work
allspp = []
for f in families:
    for s in f.spp:
        allspp.append(s)
allspp.sort(key=lambda x: x.latin_name)


def WriteIndexPage():
    doc, tag, text, line = Doc().ttl()
    doc.asis("<!DOCTYPE html>")
    with tag('html'):
        with tag('head'):
            line('title', 'My Fouine')
            doc.asis('<meta charset="utf-8">') # Important
            doc.asis('<link rel="stylesheet" href="%s">' % (stylesheet.filename))
        with tag('body'):
            line('h1', 'Bienvenue sur mon petit site de merde')
            for i in [ "Ah, quel plaisir d'humer les fleurs.",
                       "Bravo à vous, les plantes, d'avoir",
                       "rendu l'air respirable.",]:
                with tag('p'):
                    text(i)
            with tag('a', href='families.html'):
                line('p', 'Chercher par familles')
            with tag('a', href='allspp.html'):
                line('p', 'Chercher par especes')
    # Write page to disk
    writeyattag(prefix + 'index.html', doc)
    # with open(prefix + 'index.html', 'w') as file:
        # file.write(doc.getvalue())



def WriteSearchByFamilyPage():
    doc, tag, text, line = Doc().ttl()
    doc.asis("<!DOCTYPE html>")
    with tag('html'):
        with tag('head'):
            line('title', 'My Fouine')
            doc.asis('<meta charset="utf-8">') # Important   
            doc.asis('<link rel="stylesheet" href="%s">' % (stylesheet.filename))
        with tag('body'):
            with tag('ul'):
                for f in families:
                    with tag('li'):
                        with tag('a', href=f.url):
                            text(f.name)
    # Write page to disk
    writeyattag(prefix + 'families.html', doc)


def WriteSearchBySppPage():
    doc, tag, text, line = Doc().ttl()
    doc.asis("<!DOCTYPE html>")
    with tag('html'):
        with tag('head'):
            line('title', 'My Fouine')
            doc.asis('<meta charset="utf-8">') # Important
            doc.asis('<link rel="stylesheet" href="%s">' % (stylesheet.filename))
        with tag('body'):
            line('h1', 'Sorted by latin names')
            with tag('ul'):
                # Sort by latin name
                allspp.sort(key=lambda x: x.latin_name)
                for sp in allspp:
                    with tag('li'):
                        with tag('a', href=sp.url):
                            text(sp.latin_name)
            line('h1', 'Sorted by french names')
            with tag('ul'):
                # Sort by french name
                allspp.sort(key=lambda x: x.french_name)
                for sp in allspp:
                    with tag('li'):
                        with tag('a', href=sp.url):
                            text(sp.french_name)
    # Write page to disk
    writeyattag(prefix + 'allspp.html', doc)
    # with open(prefix + 'allspp.html', 'w') as file:
     #   file.write(doc.getvalue())

### WEBSITE ###

# Stylesheet
stylesheet = Stylesheet()
stylesheet.content = """

body {
  background-color: LightCyan;
}

"""
stylesheet.WriteStyleSheet()


# Write all website pages
WriteIndexPage()
WriteSearchByFamilyPage()
WriteSearchBySppPage()
for f in families:
    f.WriteFamilyIndexPage()
    for sp in f.spp:
        sp.WritePlantPage()
