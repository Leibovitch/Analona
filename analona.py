from schema import Schema, And, Or, Use, Optional, SchemaError, Regex
from dateutil import parser

class Validator(object):
    """
    General validator object
    """
    def __init__(self, item, schema):
        self.item = item
        self.schema = schema

    def run_schema(self, data):
        return(self.schema.validate(data))

    def validate_schema(self):
        try:
            self.run_schema(self.item)
        except SchemaError as x:
            return x.code
        else:
            return self.item


class BaseItem(Validator):
    """
    General valiator for single item (Ship/Plane)
    """
    def __init__(self, item, extended_schema):
        Validator.__init__(self, item, self.compose_schema(extended_schema))
    
    def get_basic_schema(self):
        return ({
            '_id': Or(str, Use(int)),
            'company': str,
            'geometry': {
                'coordinates': list,
                'type': Or("Point", "Polygon", error="geometry type: should be Point or Polygon")
            },
            'sourceItem': And(str, len),
            'observed': Use(parser.parse),
            'area': Or(float, int),
            Optional('score'): And(Use(float), lambda s: 0 <= s <= 1,error="score: should be between 0-1"),
            Optional('length'): Or(float, int),
            Optional('width'): Or(float, int),
            Optional('direction'): And(Use(float), lambda s: 0 <= s <= 360, error="direction: should be between 0-360")
        })
    
    def compose_schema(self, extended_schema):
        schema = self.get_basic_schema() 
        schema.update(extended_schema)
        return Schema(schema)

    def validate_item(self):
        return self.validate_schema()


class Ship(BaseItem):
    """
    Ship validator
    """
    def __init__(self, ship):
        BaseItem.__init__(self, ship, self.create_extended_schema())

    def create_extended_schema(self):
        return ({
            Optional('AISIdentifier'): Or(str, int)
        })

    def validate(self):
        return self.validate_item()


class Plane(BaseItem):
    """
    Airplane Validator
    """
    def __init__(self, ship):
        BaseItem.__init__(self, ship, self.create_extended_schema())

    def create_extended_schema(self):
        return ({})

    def validate(self):
        return self.validate_item()

def is_list_of_string(ids):
    is_list = True
    for item in ids:
        is_list = isinstance(item, str)
    return is_list


class BaseMap(Validator):
    """
    General validator for a raster item (Buildings, Roads, Vegetation)
    """
    def __init__(self, item, extended_schema):
        Validator.__init__(self, item, self.compose_schema(extended_schema))
    
    def get_basic_schema(self):
        url_regex = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'
        
        return ({
            '_id': Or(str, Use(int)),
            'company': str,
            Optional('geometry'): {
                'coordinates': list,
                'type': Or("Point", "Polygon", "MultiPolygon", "MultiPoint", error="geometry type error")
            },
            'provisionTime': Use(parser.parse),
            Optional('analyticsUrl'): Or(
                Regex(url_regex),
                error="analyticsUrl: invalid url"
            ),
            Optional('sourceImagesUrl'): Or(
                Regex(url_regex),
                error="sourceImagesUrl: invalid url"
            ),
            Optional('sourceImagesIds'): And(list, lambda ids: is_list_of_string(ids), error="sourceImagesIds: should be a list")
        })
    
    def compose_schema(self, extended_schema):
        schema = self.get_basic_schema() 
        schema.update(extended_schema)
        return Schema(schema)

    def validate_item(self):
        return self.validate_schema()


class Building(BaseMap):
    """
    Building Validator
    """
    def __init__(self, building):
        BaseMap.__init__(self, building, self.create_extended_schema())

    def create_extended_schema(self):
        return ({})

    def validate(self):
        return self.validate_item()


class Road(BaseMap):
    """
    Roads Validator
    """
    def __init__(self, road):
        BaseMap.__init__(self, road, self.create_extended_schema())

    def create_extended_schema(self):
        return ({})

    def validate(self):
        return self.validate_item()