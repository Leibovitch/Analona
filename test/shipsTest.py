import unittest

from datetime import datetime

from analona import Ship

class ShipTests(unittest.TestCase):
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
            "originalImageId": "20181010_075454_0f2b",
            "observed_start": datetime.strptime("2018-10-10T07:54:54.908391Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
            "observed_end": datetime.strptime("2018-10-10T07:54:54.908391Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
            "creation_time": datetime.strptime("2019-01-16T07:54:54.908391Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
            "update_time": datetime.strptime("2019-01-16T07:54:54.908391Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
            "area": 1787.9730195193133,
            "score": 0.7,
            "length": 2000,
            "width": 1000,
            "AISIdentifiers": {
                "IMO": "Aa123"
            }
        }

    def test_validShip_shouldPass(self):
        res = Ship(self.data)
        self.assertTrue(res.validate())

    def test_badScore_shouldNotPass(self):
        bad_score = self.data
        bad_score["score"] = 1.7
        res = Ship(bad_score)
        self.assertEqual(res.validate(), "score: should be between 0-1")


if __name__ == '__main__':
    unittest.main()
