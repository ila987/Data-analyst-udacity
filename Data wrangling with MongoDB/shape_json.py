#this function reads the complete osm files, 
#it corrects the point found in the audit part and it creates a json file
#that can be used to load it to the DB


#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

"""
osm_file = open("milan_italy.osm", "r")

#Dictionary used to fix the wrong postcodes found in the audit part
postcodes_tofix = {
    "2090":"20090",
    "2121":"20121",
    "2043":"20143",
    "2014":"20124",
    "2009":"20092",
    "2003":"20030"
}

#function to correct postcodes
def correct_postcode(postcode):
    for wrongcode, correctedcode in postcodes_tofix.iteritems():
        if wrongcode == postcode:
            return correctedcode

#function to standardize contacts information to have a tag "contact:X" instead of just X
#creating such a correspondency it would allow us to then create a dictionary containing just
#contact information
def correct_contact_type(contact_type):
    return "contact:"+ contact_type

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'\"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

NODE = ["id", "version", "visible", "changeset", "timestamp", "user", "uid", "lat", "lon"]

WAY = ["id", "version", "visible", "changeset", "timestamp", "user", "uid"]

#Shape function that read nodes and ways and creates dictionaries as explained above
def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag =="way":
        created={}
        pos = [0,0]
        #create a key for each attribute
        for n in element.attrib:
            #if the attribute is in the created dictionary, then create a separate dictionary
            if n in CREATED:
                created[n]=element.attrib[n]
            else:
                #put longitude and latidute as an array
                if n in ["lon", "lat"]:
                    if n in ["lon"]:
                        pos[1]= (float(element.attrib[n]))
                    if n in ["lat"]:
                        pos[0]= (float(element.attrib[n]))
                else:
                    node[n]= element.attrib[n]
        node['type']=element.tag
        node['created']= created
        node['pos'] = pos
        address={}
        contact= {}
        #explore the child of the element
        for child in element.iter("tag"):
            if re.search(problemchars, child.attrib['k']):
                pass
            #if it's an address, create a dictionary with all information about it 
            if child.attrib['k'].startswith('addr:'):
                if child.attrib['k'].count(':') ==1:
                    address[child.attrib['k'][5:]] = child.attrib['v']
            #if it's a contact info, create a dictionary with all those values
            if child.attrib['k'].startswith('contact:'):
                contact[child.attrib['k'][8:]] = child.attrib['v']
            else:
                node[child.attrib['k'].split(':')[0]] = child.attrib['v']
        if address:
            node["address"] = address
        if contact:
            node["contact"] = contact
        node_refs = []
        for tag in element.iter("nd"):
            node_refs.append(tag.attrib['ref'])
            node['node_refs'] = node_refs
                
        return node
    
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, elem in ET.iterparse(file_in):
            if is_mail_contact(elem):
                elem.attrib['k'] = correct_contact_type(elem.attrib['k'])
            #print elem.attrib['k']
            if is_fax_contact(elem):
                elem.attrib['k'] = correct_contact_type(elem.attrib['k'])
            #print elem.attrib['k']
            if is_phone_contact(elem):
                elem.attrib['k'] = correct_contact_type(elem.attrib['k'])
            #print elem.attrib['k']
            if is_website_contact(elem) or is_url_contact(elem):
                elem.attrib['k'] = correct_contact_type(elem.attrib['k'])
            #print elem.attrib['k']
            if is_postcode_name(elem) and elem.attrib['v'] in postcodes_tofix.keys():
                elem.attrib['v'] = correct_postcode(elem.attrib['v'])
            
            el = shape_element(elem)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    fo.close()
    return data

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map(osm_file, True)
    #pprint.pprint(data)
    
    
if __name__ == "__main__":
    test()
