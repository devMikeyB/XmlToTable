from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
import csv
import luadata as lua
from typing import Dict
#import requests
import xml.etree.ElementTree as ET


def parseXML(xmlfile): # Parses the XML file and returns a list of all the children of the root element.
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    return root

def getTieredItems(xmlfile, tier): # Returns a list of all the items in the XML file that are in the specified tier.
    workableData = parseXML(xmlfile)
    workableTable = []
    tierRequests = []
    
    for child in workableData: # Loops through the children of the root element.
        if(child.tag == 'Object'):
            for attribute in child: # Loops through the attributes of the child.
                if(attribute.tag == 'Class' and attribute.text == 'Equipment'): # If the attribute is an equipment item.

                    workableTable.append(child) # Adds the child to the list of items.
    
    for Equipment in workableTable: # Loops through the items in the list.
        for child in Equipment: # Loops through the children of the item.
            if child.tag == 'Tier': 
                if child.text == str(tier): # If the item is in the specified tier.
                    tierRequests.append(Equipment) # Adds the item to the list of items in the tier.

    #tierDict = dict(tierRequests)
    #print(tierDict)

    tierDict = {}
    i = 0
    for Equipment in tierRequests:
        equipName = Equipment.attrib.get('id')
        for child in Equipment:
            if child.tag == 'Description':
                equipDesc = child.text
            if child.tag == 'Tier':
                equipTier = child.text
            if child.tag == 'SlotType':
                equipSlotType = child.text
            if child.tag == 'BagType':
                equipBagType = child.text
            #if child.tag == 'Usable':
            #    equipUsable = 1
            #if child.tag == 'Range':
            #    equipRange = child.text
            #if child.tag == 'MPCost':
            #    equipManaCost = child.text
            #if child.tag == 'Duration':
            #    equipDuration = child.text
            #equipCooldown = 0

        tierDict[i] = {
            'equipName': equipName,
            'equipDesc': equipDesc,
            'equipTier': equipTier,
            'equipSlotType': equipSlotType,
            'equipBagType': equipBagType,
            #'equipUsable': equipUsable,
            #'equipRange': equipRange,
            #'equipManaCost': equipManaCost,
            #'equipDuration': equipDuration,
            #'equipCooldown': equipCooldown
        }
        i += 1

    

    return tierDict  

print("Enter Tier of items to export: ")
tier=input()

testXMLSAMPLE = getTieredItems('test.xml', tier)

print(testXMLSAMPLE)
lua.write('tier'+str(tier)+"Items.lua", testXMLSAMPLE)
