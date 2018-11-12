from schema import Schema, And, Or, Use, Optional 
from dateutil import parser

schema = Schema(
  {
    '_id': Or(str, Use(int)),
    'company': str,
    'geometry': {
      'coordinates': list,
      'type': Or("Point", "Polygon")
    },
    'sourceItem': And(str, len),
    'observed': Use(parser.parse),
    'area': Or(float, int),
    Optional('score'): And(Use(float), lambda s: 0 <= s <= 1),
    Optional('length'): Or(float, int),
    Optional('width'): Or(float, int),
    Optional('direction'): And(Use(float), lambda s: 0 <= s <= 360)
  }
)
