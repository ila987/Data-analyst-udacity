#This file reads the osm files and looks for anomalies in the data
#In particular, it analyses postcodes and how contacts information are 
#saved in the file


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
from collections import defaultdict
import re

osm_file = open("milan_italy.osm", "r")

#phone, fax, website, url, should all become contact:X
#fix elem.attrib['k']=url, website and change it to "contact:website"

#TO DO change label gym, lotto, nightclub, picnic_table from amenity to leisure
#change 14 restaurant under building

#regex to check postal code that have <5 digits
postcode_type_re = re.compile(r'^\d{1,4}$', re.IGNORECASE)

#dictionaries for all wrong codes and contacts info
wrong_mails = defaultdict(int)
wrong_faxes = defaultdict(int)
wrong_phones = defaultdict(int)
wrong_websites = defaultdict(int)
wrong_postcodes = defaultdict(int)
wrong_postcodes_cities = []

#this function adds to a dictionary the wrong postcode (<5 digits)
def audit_postcode_type(wrong_postcode, postcode):
    r = postcode_type_re.search(postcode)
    if r:
        wrong_postcode = r.group()
        wrong_postcodes[wrong_postcode] += 1

#this function adds to a dictionary the contacts information that are stored in a wrong way
def audit_contact_type(contact_types, name):
    contact_types[name] += 1

def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v) 

#helper functions to check types of tag
def is_mail_contact(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "mail")

def is_fax_contact(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "fax")

def is_phone_contact(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "phone")

def is_website_contact(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "website")

def is_url_contact(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "url")

def is_postcode_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:postcode")


#audit functions that checks for wrong postcodes and contact info (mail, fax, phone, website) stored wrongly
def audit():
    for event, elem in ET.iterparse(osm_file):
        if is_mail_contact(elem):
            audit_contact_type(wrong_mails, elem.attrib['v'])
        if is_fax_contact(elem):
            audit_contact_type(wrong_faxes, elem.attrib['v'])
        if is_phone_contact(elem):
            audit_contact_type(wrong_phones, elem.attrib['v'])
        if is_website_contact(elem) or is_url_contact(elem):
            audit_contact_type(wrong_websites, elem.attrib['v'])
        if is_postcode_name(elem):
            audit_postcode_type(wrong_postcodes, elem.attrib['v'])
    print_sorted_dict(wrong_postcodes)
    print_sorted_dict(wrong_mails)
    print_sorted_dict(wrong_faxes)
    print_sorted_dict(wrong_phones)
    print_sorted_dict(wrong_websites)
    


if __name__ == '__main__':
    audit()
