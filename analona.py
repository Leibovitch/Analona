from schema import Schema, And, Or, Use, Optional, SchemaError
from dateutil import parser

class Validator(object):
    """
    General validtor object
    """
    def __init__(self, item, schema):
        self.item = item
        self.schema = schema

    def run_schema(self, data):
        return(self.schema.validate(data))

    def validate_item(self):
        try:
            self.run_schema(self.item)
        except SchemaError as x:
            return x.code
        else:
            return self.item

class Ship(Validator):
    """
    Ship validator
    """
    def __init__(self, ship):
        Validator.__init__(self, ship, self.create_schema())

    def create_schema(self):
        return (
            Schema({
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
                Optional('direction'): And(Use(float), lambda s: 0 <= s <= 360, error="direction: should be between 0-360"),
                Optional('AISIdentifier'): Or(str, int)
            })
        )

    def validate(self):
        return self.validate_item()


class Plane(Validator):
    """
    Airplane Validator
    """
    def __init__(self, plane):
        Validator.__init__(self, plane, self.create_schema())

    def create_schema(self):
        return (
            Schema({
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
        )

    def validate(self):
        return self.validate_item()


