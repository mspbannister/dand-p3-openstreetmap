"""
Collection of functions to enable auditing and cleaning of street type and post code values 
for OSM London data. 
Mappings based on findings from analysis of data sample.

Adapted from Udacity quizzes by Mark Bannister
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
"""Regular expression to recognise street type."""

post_code_re = re.compile(r'[A-Z]{1,2}\d{1,2}[A-Z]? \b\d[A-Z]{2,2}', re.IGNORECASE)
"""Regular expression to recognise valid post codes.
   Examples: "E9 6JQ", "E14 9GE" "W1W 6PB", "SW1P 3PS".
"""

short_post_code_re = re.compile(r'[A-Z]{1,2}\d{1,2}[A-Z]?\b', re.IGNORECASE)
"""Regular expression to recognise valid short post codes.
   Examples: "E9", "E14", "W1W", "SW1P".
"""

expected_street_types = ["Street", "Avenue", "Drive", "Court", "Place", "Square", "Lane", 
                         "Road", "Mews", "Market", "Close", "Gardens", "Grove", "Crescent",
                         "Buildings", "Green", "Hill", "Terrace", "Acre", "Churchyard", 
                         "Fields", "Row", "Walk", "Way", "Park", "Yard", "Wharf", "Villas", 
                         "Vale", "Parade", "Passage", "Gate", "Broadway", "Approach", "Rise", 
                         "Bridge", "Circus", "Quay", "Docks"]


def audit_street_type(street_types, street_name):
    """Build defaultdict of unexpected street types.
    Args:
        street_types (dict): defaultdict(set) of unexpected street types.
        street_name (str): street name data.
    """
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected_street_types:
            street_types[street_type].add(street_name)
            
def audit_post_codes(post_codes, post_code):
    """Build set of unexpected post codes.
    Args:
        post_codes (set): unexpected post codes.
        post_code (str): post code data.
    """
    m = post_code_re.match(post_code)
    if not m:
        post_codes.add(post_code)

def is_street_name(elem):
    """Determine whether street name data.
    Args:
        elem (obj): element found using ET.iterparse().
    Returns:
        True for success, False otherwise.
    """
    return (elem.attrib['k'] == "addr:street")

def is_post_code(elem):
    """Determine whether post code data.
    Args:
        elem (obj): element found using ET.iterparse().
    Returns:
        True for success, False otherwise.
    """
    return (elem.attrib['k'] == "addr:postcode")

def audit(osmfile):
    """Audit street type and post code data.
    Args:
        osmfile (obj): OSM (XML) file to audit.
    Returns:
        street_types (dict): defaultdict(set) of unexpected street types.
        post_codes (set): unexpected post codes.
    """
    osm_file = open(osmfile, "rb")
    street_types = defaultdict(set)
    post_codes = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                elif is_post_code(tag):
                    audit_post_codes(post_codes, tag.attrib['v'])
    osm_file.close()
    return street_types, post_codes