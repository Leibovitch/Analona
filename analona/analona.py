from schema import Schema, And, Or, Use, Optional, SchemaError, Regex
from datetime import datetime

class Validator(object):
    """
    General validator object
    """

    def __init__(self, item, schema = {}):
        self.item = item
        self.schema = Schema(schema)

    def validate(self):
        try:
            self.schema.validate(self.item)
        except SchemaError as x:
            return x.code
        else:
            return True

    def get_schema(self):
        # each child class should implement this method
        return self.schema

    def compose_schema(self):
        # if a child class want to extend schema is should override this method
        schema = self.get_schema()
        return Schema(schema)

class BaseDetection(Validator): 
    """
    General validator for a single detection (Ship/Plane)
    """

    url_regex = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'
    storage_regex = r'(gs|s3)?://[-a-zA-Z0-9@:%._\+~#=]{2,256}/([\w\+~#=-]*/)*'
    unique_parameters = {
            '_id': Or(str, Use(int)),
            'collection': Or("ships", "buildings", "roads", "vegetation", "planes", error="analyticsInfo: unknowen collection name"),
            'company': Or("Planet", "OrbitalInsight", "SpaceKnow", "RadiantSolutions", error="analyticsInfo: unknown company name"),
            'observed_start': datetime, 
            'observed_end': datetime,
            'creation_time': datetime,
            'update_time': datetime,
            Optional('tile_id'): {
                "row": Or(str, Use(int)),
                "col": Or(str, Use(int)),
                "full_id": str
            },
            Optional('linkToSourceObject'): {
                "url": Or(Regex(url_regex), Regex(storage_regex), error="analyticsInfo: invalid url"),
                "storage": Or("Azure", "AWS", "GoogleCloud", "Planet", error="analyticsInfo: unknown storage type")
        }
    }

    @staticmethod
    def compose_schema(schema):
        schema.update(BaseDetection.unique_parameters)
        return schema

    def __init__(self, item, schema = {}):
        super().__init__(item, BaseDetection.compose_schema(schema))



class BaseObject(BaseDetection):
    """
    General validator for single item (Ship/Plane)
    """
    unique_parameters = {
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

    @staticmethod   
    def compose_schema(schema):
        schema.update(BaseObject.unique_parameters)
        return schema

    def __init__(self, item, schema = {}):
        super().__init__(item, BaseObject.compose_schema(schema))

class Ship(BaseObject):
    """
    Ship validator
    """

    unique_parameters = {
        Optional('AISIdentifiers'): {
            Optional('IMO'): Or(str, int),
            Optional('GUID'): Or(str, int)
        }
    }

    def __init__(self, item, schema = {}):
        super().__init__(item, Ship.compose_schema(schema))
    
    @staticmethod
    def compose_schema(schema):
        schema.update(Ship.unique_parameters)
        return schema

class Plane(BaseObject):
    """
    Airplane Validator
    """
    unique_parameters = {}

    @staticmethod
    def compose_schema(schema):
        schema.update(BaseObject.unique_parameters)
        return schema

    def __init__(self, item, schema = {}):
        super().__init__(item, Plane.compose_schema(schema))


def is_list_of_strings(ids):
    return all([isinstance(item, str) for item in ids])


class BaseMap(BaseDetection):
    """
    General validator for a raster item (Buildings, Roads, Vegetation)
    """
    unique_parameters = {
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

    def __init__(self, item, schema = {}):
        super().__init__(item, BaseMap.compose_schema(schema))

    @staticmethod
    def compose_schema(schema):
        schema.update(BaseMap.unique_parameters)
        return schema

class Building(BaseMap):
    """
    Building Validator
    """
    unique_parameters = {}

    @staticmethod
    def compose_schema(schema):
        schema.update(BaseMap.unique_parameters)
        return schema

    def __init__(self, item, schema = {}):
        super().__init__(item, Building.compose_schema(schema))

class Road(BaseMap):
    """
    Roads Validator
    """
    unique_parameters = {}

    @staticmethod
    def compose_schema(schema):
        schema.update(BaseMap.unique_parameters)
        return schema

    def __init__(self, item, schema = {}):
        super().__init__(item, Road.compose_schema(schema))


class Vegetation(BaseMap):
    """
    Vegetation Validator
    """
    unique_parameters = {}

    @staticmethod
    def compose_schema(schema):
        schema.update(BaseMap.unique_parameters)
        return schema

    def __init__(self, item, schema = {}):
        super().__init__(item, Vegetation.compose_schema(schema))

class SchemeException(Exception):
    pass
