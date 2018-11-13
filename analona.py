from schema import Schema, And, Or, Use, Optional, SchemaError
from dateutil import parser


class Ship(object):
    """
    Ship validator
    """
    def __init__(self, ship):
        self.ship = ship

    def run_schema(self, data):
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
            }).validate(data)
        )

    def validate(self):
        try:
            self.run_schema(self.ship)
        except SchemaError as x:
            return x.code
        else:
            return self.ship


class Plane(object):
    """
    Airplane Validator
    """
    def __init__(self, plane):
        self.plane = plane

    def run_schema(self, data):
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
            }).validate(data)
        )

    def validate(self):
        try:
            self.run_schema(self.plane)
        except SchemaError as x:
            return x.code
        else:
            return self.plane