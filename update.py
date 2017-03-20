"""
Collection of functions to enable cleaning of relevant values for OSM London data. 
Mappings based on findings from analysis of data sample.

Author: Mark Bannister
"""

from audit_address import street_type_re, post_code_re, short_post_code_re
import re

                        
amenity_mapping = { "currency_exchange": "bureau_de_change",
                    "market": "marketplace",
                    "social_centre": "social_facility",
                    "ticket_booth": "ticket_office" }

cuisine_mapping = { "Bangladeshi": "bangladeshi",
                    "Caribbean": "caribbean",
                    "fried_chicken": "chicken",
                    "Juices": "juices",
                    "modern european": "modern_european",
                    "steak_house": "steak",
                    "Surf_and_Turf": "seafood",
                    "Vegan": "vegan" }
                    
street_type_mapping = { "Rd.": "Road",
                        "Rd": "Road",
                        "St": "Street",
                        "St.": "Street" }

shop_type_mapping = { "accessories": "fashion_accessories",
                      "bag": "fashion_accessories",
                      "bathroom": "bathroom_furnishing",
                      "beauty_salon": "beauty",
                      "bppkmaker": "bookmaker",
                      "communication": "communications",
                      "dry_cleaning": "dry_cleaner",
                      "electrical": "electronics",
                      "healthfood": "health_food",
                      "houseware": "household",
                      "jewelry": "jewellery",
                      "market": "marketplace",
                      "nail": "nails",
                      "perfumery": "perfume",
                      "plumbing": "plumbing_supplies",
                      "radiotechnics": "electronics",
                      "tile": "tiles" }

def update_amenity(value):
    """Clean amenity values based on mapping.
    Args:
        value (str): raw amenity value.
    Returns:
        value (str): cleaned amenity value.
    """
    if value in amenity_mapping:
        value = amenity_mapping[value]
    return value
    
def update_cuisine(value):
    """Clean cuisine values based on mapping.
    Args:
        value (str): raw cuisine value.
    Returns:
        value (str): cleaned cuisine value.
    """
    if value in cuisine_mapping:
        value = cuisine_mapping[value]
    return value

def update_street_name(value):
    """Clean street name values based on mapping.
    Args:
        value (str): raw street name value.
    Returns:
        value (str): cleaned street name value.
        None if data does not match expected format.
    """
    m = street_type_re.search(value)
    if m:
        if m.group() in street_type_mapping:
            startpos = value.find(m.group())
            value = value[:startpos] + street_type_mapping[m.group()]
        return value
    else:
        return None
    
def update_post_code(value):
    """Clean post code values based on expected format.
    Args:
        value (str): raw post code value.
    Returns:
        value (str): raw post code value.
        None if data does not match expected format.
    """
    if not post_code_re.match(value):
        m = short_post_code_re.match(value)
        if m:
            value = m.group()
        else:
            return None
    return value

def update_shop_type(value):
    """Clean shop type values based on mapping.
    Args:
        value (str): raw shop type value.
    Returns:
        value (str): cleaned shop type value.
    """
    if value in shop_type_mapping:
        value = shop_type_mapping[value]
    return value
                        
def update_value(value, key):
    """Determine whether value needs cleaning and apply relevant function as required.
    Args:
        value (str): raw data value.
        key (str): paired key denoting data type e.g. "amenity".
    Returns:
        value (str): data value cleaned according to relevant function
        value (str): raw data value if cleaning not required.
    """
    if key == "amenity":
        return update_amenity(value)
    elif key == "cuisine":
        return update_cuisine(value)
    elif key == "addr:street":
        return update_street_name(value)
    elif key == "addr:postcode":
        return update_post_code(value)
    elif key == "shop:type":
        return update_shop_type(value)
    else:
        return value
                       
def update_type(key):
    """Clean 'type' keys as required.
    Args:
        key (str): raw 'type' key.
    Returns:
        key (str): cleaned 'type' key.
    """
    if ":type" in key:
         pass
    elif "_type" in key:
         key = key[:(key.find("_type"))] + ":type"
    elif "type" in key and key.find("type") != 0:
         key = key[:(key.find("type"))] + ":type"
    return key