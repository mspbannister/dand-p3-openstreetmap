"""
Collection of functions to enable cleaning of relevant values for OSM London data. 
Mappings based on findings from analysis of data sample.

Authors: Mark Bannister (shape_element), Udacity (get_element, validate_element, process_map)
"""

import unicodecsv
import pprint
import re
import xml.etree.cElementTree as ET
import cerberus
import schema
import update

OSM_FILE = "central_London_sample.osm" # Replace with your OSM file

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
"""Regular expression to recognise problem characters"""

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'category']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'category']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_category='regular'):
    """Clean and shape node or way XML element to Python dict.
    Args:
        element (obj): element found using ET.iterparse().
        node_attr_fields (list): node attribute fields to be passed to output dict
        way_attr_fields (list): way attribute fields to be passed to output dict
        problem_chars (regex): regular expression to recognise problem characters
        default_tag_category (str): default value to be passed to the 'category' 
            field in output dict
    Returns:
        dict of node/way element attributes and attributes of child elements (tags)
        format if node: {'node': node_attribs, 'node_tags': tags}
        format if way: {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}
    """

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    nd_position = -1
    
    for child in element:
        if child.tag == 'tag':
            # Clean 'k' value to ensure those reflecting "type" are properly handled later
            key_attrib = update.update_type(child.attrib['k'].strip())
            if not PROBLEMCHARS.search(key_attrib):
                tag = {'category': default_tag_category}
                tag['id'] = element.attrib['id'].strip()
                # Creating separate "amenity" tag for shops while incorporating "type" data
                if key_attrib == "shop":
                    key_attrib = "shop:type"
                    tag['key'] = "amenity"
                    tag['value'] = "shop"
                    tags.append(tag.copy())
                # Separate key prefixes into "category" data
                key_colon = key_attrib.find(':')
                if key_colon > 0:
                    tag['key'] = key_attrib[(key_colon + 1):]
                    tag['category'] = key_attrib[:(key_colon)]
                else:
                    tag['key'] = key_attrib          
                # Clean values and unpack list data where required
                previous_values = []
                for entry in child.attrib['v'].split(";"):
                    value = update.update_value(entry.strip(), key_attrib)
                    if value and value not in previous_values:
                        tag['value'] = value
                        tags.append(tag.copy())
                        previous_values.append(value)
                    else:
                        pass
                
        if child.tag == 'nd':
            nd_position += 1
            way_node = {}
            way_node['id'] = element.attrib['id'].strip()
            way_node['node_id'] = child.attrib['ref'].strip()
            way_node['position'] = nd_position
            way_nodes.append(way_node)
            
    if element.tag == 'node':
        for field in NODE_FIELDS:
            node_attribs[field] = element.attrib[field].strip()
        return {'node': node_attribs, 'node_tags': tags}
    
    elif element.tag == 'way':
        for field in WAY_FIELDS:
            way_attribs[field] = element.attrib[field].strip()
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag.
    Args:
        osmfile (obj): OSM (XML) file to audit.
        tags (list): element types to be yielded,
    Yields:
        elem (obj): element found using ET.iterparse().
    """
    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema.
    Args:
        element (dict): dict of node/way element attributes and attributes of child elements
            returned by shape_element()
        validator (obj): cerberus.Validator object
        schema (dict): schema of desired data structure
    Raises:
        exception if element structure does not match schema
    """
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate=False):
    """Iteratively process each XML element and write to csv(s).
    Args:
        file_in (obj): OSM (XML) file to audit.
        validate (bool): if True, will validate each element using validate_element()
    Returns:
        five CSV files containing data for node, node tag, way, way tag and way node type
            elements
    """

    with open(NODES_PATH, 'wb') as nodes_file, \
         open(NODE_TAGS_PATH, 'wb') as nodes_tags_file, \
         open(WAYS_PATH, 'wb') as ways_file, \
         open(WAY_NODES_PATH, 'wb') as way_nodes_file, \
         open(WAY_TAGS_PATH, 'wb') as way_tags_file:

        nodes_writer = unicodecsv.DictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = unicodecsv.DictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = unicodecsv.DictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = unicodecsv.DictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = unicodecsv.DictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])
                    
process_map(OSM_FILE)