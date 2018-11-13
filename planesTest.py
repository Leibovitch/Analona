from analona import Plane

example = {
    "_id" : "feea0196-b6b9-45a7-a7ba-a67287236e06",
    "company": "Planet",
    "geometry" : {
        "coordinates" : [
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
        "type" : "Polygon"
    },
    "sourceItem" : "20181010_075454_0f2b",
    "observed" : "2018-10-10T07:54:54.908391Z",
    "area": 1787.9730195193133,
    "score": 0.7, 
    "length": 2000, 
    "width": 1000
}

res = Plane(example)
assert(res.validate() == example)

bad_score = example
bad_score["score"] = 1.7
res = Plane(bad_score)
assert(res.validate() == "score: should be between 0-1")

