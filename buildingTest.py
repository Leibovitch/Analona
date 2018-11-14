from analona import Building

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
    "analyticsUrl" : "http://planet.com/abcd",
    "provisionTime" : "2018-10-10T07:54:54.908391Z",
    "sourceImagesIds": ["id_1", "id_2"]
}

res = Building(example)
assert(res.validate() == example)

bad_ids = example
bad_ids["sourceImagesIds"] = [1, 2]
res = Building(bad_ids)
assert(res.validate() == "sourceImagesIds: should be a list")

bad_url = example
bad_url["analyticsUrl"] = "1234://not.url"
res = Building(bad_url)
assert(res.validate() == "analyticsUrl: invalid url")

