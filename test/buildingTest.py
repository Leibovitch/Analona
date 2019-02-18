import unittest

from datetime import datetime

from analona import Building

class BuildingTests(unittest.TestCase):
    def setUp(self):
        self.data = {
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

    def test_validBuilding_shouldPass(self):
        res = Building(self.data)
        self.assertTrue(res.validate())

    def test_badIds_shouldNotPass(self):
        bad_ids = self.data
        bad_ids["sourceImagesIds"] = [1, "2"]
        res = Building(bad_ids)
        self.assertEqual(res.validate(), "sourceImagesIds: should be a list")

    def test_badUrl_shouldNotPass(self):
        bad_url = self.data
        bad_url["linkToSourceObject"]["url"] = "1234://not.url"
        res = Building(bad_url)
        self.assertEqual(res.validate(), "analyticsInfo: invalid url")


if __name__ == '__main__':
    unittest.main()
