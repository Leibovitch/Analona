from schema import Schema, And, Or, Use, Optional, SchemaError, Regex
from datetime import datetime

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

class BaseDetection(Validator): 
    """
    General valiator for a single detection (Ship/Plane)
    """

    url_regex = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'
    storage_regex = r'(gs|s3)?://[-a-zA-Z0-9@:%._\+~#=]{2,256}/([\w\+~#=-]*/)*'

    def __init__(self, item):
        Validator.__init__(self, item, self.compose_schema())


    def get_schema(self):
        return ({
            '_id': Or(str, Use(int)),
            'company': str,
            'observed_start': datetime, 
            'observed_end': datetime,
            Optional('tileId'): {
                "row": Or(str, Use(int)),
                "col": Or(str, Use(int)),
                "full_id": str
            },
            Optional('linkToSourceObjext'): {
                "url": Or(Regex(BaseDetection.url_regex), Regex(BaseDetection.storage_regex), error="analyticsInfo: invalid url"),
                "storage": Or("Azure", "AWS", "GoogleCloud", "Planet", error="analyticsInfo: unknown storage type")
            }
        })

class BaseObject(BaseDetection):
    """
    General valiator for single item (Ship/Plane)
    """
    def __init__(self, item):
        Validator.__init__(self, item, self.compose_schema())
    
    def comopse_schema(self):
        schema = self.get_schema()
        additional_parameters = {
            'geometry': {
                'coordinates': list,
                'type': Or("Point", "Polygon", error="geometry type: should be Point or Polygon")
            },
            'originalImageId': And(str, len),
            'area': Or(float, int),
            'length': Or(float, int),
            'width': Or(float, int),
            Optional('score'): And(Use(float), lambda s: 0 <= s <= 1,error="score: should be between 0-1"),
            Optional('direction'): And(Use(float), lambda s: 0 <= s <= 360, error="direction: should be between 0-360")
            
        }
        schema.update(additional_parameters)
        return Schema(schema)


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


class BaseMap(BaseDetection):
    """
    General validator for a raster item (Buildings, Roads, Vegetation)
    """
    def __init__(self, item):
        Validator.__init__(self, item, self.compose_schema())
    
    def compose_schema(self):
        schema = self.get_schema()
        additional_parameters = {
            'geometry': {
                'coordinates': list,
                'type': Or("Point", "Polygon", "MultiPolygon", "MultiPoint", error="geometry type error")
            },

            Optional('sourceImagesInfo'): {
                "url": Or(Regex(BaseDetection.url_regex), Regex(BaseDetection.storage_regex), error="sourceImagesInfo: invalid url"),
                "storage": Or("Azure", "AWS", "GoogleCloud", error="sourceImagesInfo: unknown storage type")
            },

            Optional('sourceImagesIds'): And(list, lambda ids: is_list_of_strings(ids), error="sourceImagesIds: should be a list")
        }
        schema.update(additional_parameters)
        return Schema(schema)


class Building(BaseMap):
    """
    Building Validator
    """
    def __init__(self, building):
        BaseMap.__init__(self, building)


class Road(BaseMap):
    """
    Roads Validator
    """
    def __init__(self, road):
        BaseMap.__init__(self, road)


class Vegetation(BaseMap):
    """
    Vegetation Validator
    """
    def __init__(self, vegetation):
        BaseMap.__init__(self, vegetation)