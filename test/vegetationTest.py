from datetime import datetime
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from analona import Vegetation

example = {
    "_id": "feea0196-b6b9-45a7-a7ba-a67287236e06",
    "company": "SpaceKnow",
    "geometry": {
        "coordinates": [
            [
                [
                    32.5088182750295,
                    29.9170847806597
                ],
                [
                    32.5088210610498,
                    29.9165171488117
                ],
                [
                    32.5085265907973,
                    29.9165160516762
                ],
                [
                    32.5085238031069,
                    29.9170836834992
                ],
                [
                    32.5088182750295,
                    29.9170847806597
                ]
            ]
        ],
        "type": "Polygon"
    },
    "analyticsInfo": {
        "url": "gs://spaceknow-customer46-delivery/weekly/aoi-1/r00c06/2018W45/20181115T072837_LANc",
        "storage": "GoogleCloud"
    },
    "observed_start": datetime.strptime("2018-10-10T07:54:54.908391Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
    "observed_end": datetime.strptime("2018-10-16T07:54:54.908391Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
    "sourceImagesIds": ["id_1", "id_2"]
}

res = Vegetation(example)
assert(res.validate() == True)

bad_ids = example
bad_ids["sourceImagesIds"] = [1, 2]
res = Vegetation(bad_ids)
assert(res.validate() == "sourceImagesIds: should be a list")

bad_url = example
bad_url["analyticsInfo"]["url"] = "1234://not.url"
res = Vegetation(bad_url)
assert(res.validate() == "analyticsInfo: invalid url")

