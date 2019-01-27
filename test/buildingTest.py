from datetime import datetime
import os,sys,inspect
import pprint

pp = pprint.PrettyPrinter(indent=4)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from analona import Building

def run_test():
    example = {
        "_id": "feea0196-b6b9-45a7-a7ba-a67287236e06",
        "company": "Planet",
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
        "linkToSourceObject": {
            "url": "http://planet.com/abcd",
            "storage": "Azure"
        },
        "creation_time": datetime.strptime("2019-01-16T07:54:54.908391Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
        "update_time": datetime.strptime("2019-01-16T07:54:54.908391Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
        "observed_start": datetime.strptime("2018-10-10T07:54:54.908391Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
        "observed_end": datetime.strptime("2018-10-16T07:54:54.908391Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
        "sourceImagesIds": ["id_1", "id_2"]
    }

    res = Building(example)
    assert(res.validate() == True)

    bad_ids = example
    bad_ids["sourceImagesIds"] = [1, "2"]
    res = Building(bad_ids)
    assert(res.validate() == "sourceImagesIds: should be a list")

    bad_url = example
    bad_url["linkToSourceObject"]["url"] = "1234://not.url"
    res = Building(bad_url)
    assert(res.validate() == "analyticsInfo: invalid url")

run_test()