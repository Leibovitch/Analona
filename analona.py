from schema import Schema, And, Or, Use, Optional, SchemaError, Regex
from dateutil import parser

class Validator(object):
    """
    General validator object
    """
    def __init__(self, item, schema):
        self.item = item
        self.schema = schema

    def validate(self):
        try:
            self.schema.validate(self.item)
        except SchemaError as x:
            return x.code
        else:
            return True

    def get_schema(self):
        # each child class should implement this method
        return ({})

    def compose_schema(self):
        # if a child class want to extend schema is should override this method
        schema = self.get_schema()
        return Schema(schema)


class BaseObject(Validator):
    """
    General valiator for single item (Ship/Plane)
    """
    def __init__(self, item):
        Validator.__init__(self, item, self.compose_schema())
    
    def get_schema(self):
        return ({
            '_id': Or(str, Use(int)),
            'company': str,
            'geometry': {
                'coordinates': list,
                'type': Or("Point", "Polygon", error="geometry type: should be Point or Polygon")
            },
            'originalImageId': And(str, len),
            'observed': Use(parser.parse),
            'area': Or(float, int),
            Optional('score'): And(Use(float), lambda s: 0 <= s <= 1,error="score: should be between 0-1"),
            Optional('length'): Or(float, int),
            Optional('width'): Or(float, int),
            Optional('direction'): And(Use(float), lambda s: 0 <= s <= 360, error="direction: should be between 0-360")
        })


class Ship(BaseObject):
    """
    Ship validator
    """
    def __init__(self, ship):
        BaseObject.__init__(self, ship)
    
    def compose_schema(self):
        schema = self.get_schema()
        additional_parameters = {
            Optional('AISIdentifiers'): {
                Optional('IMO'): Or(str, int),
                Optional('IMO'): Or(str, int),
                Optional('GUID'): Or(str, int)
            }
        } 
        schema.update(additional_parameters)
        return Schema(schema)

class Plane(BaseObject):
    """
    Airplane Validator
    """
    def __init__(self, ship):
        BaseObject.__init__(self, ship)


def is_list_of_strings(ids):
    return all([isinstance(item, str) for item in ids])


class BaseMap(Validator):
    """
    General validator for a raster item (Buildings, Roads, Vegetation)
    """
    def __init__(self, item, extended_schema):
        Validator.__init__(self, item, self.compose_schema())
    
    def get_schema(self):
        url_regex = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'
        
        return ({
            '_id': Or(str, Use(int)),
            'company': str,
            Optional('geometry'): {
                'coordinates': list,
                'type': Or("Point", "Polygon", "MultiPolygon", "MultiPoint", error="geometry type error")
            },
            'provisionTime': Use(parser.parse),
            Optional('analyticsInfo'): {
                "url": Or(Regex(url_regex), error="analyticsInfo: invalid url"),
                "storage": Or("Azure", "AWS", "GoogleCloud", error="analyticsInfo: unknown storage type")
            },
            Optional('sourceImagesInfo'): {
                "url": Or(Regex(url_regex), error="sourceImagesInfo: invalid url"),
                "storage": Or("Azure", "AWS", "GoogleCloud", error="sourceImagesInfo: unknown storage type")
            },
            Optional('sourceImagesIds'): And(list, lambda ids: is_list_of_strings(ids), error="sourceImagesIds: should be a list")
        })


class Building(BaseMap):
    """
    Building Validator
    """
    def __init__(self, building):
        BaseMap.__init__(self, building, self.compose_schema())


class Road(BaseMap):
    """
    Roads Validator
    """
    def __init__(self, road):
        BaseMap.__init__(self, road, self.compose_schema())

