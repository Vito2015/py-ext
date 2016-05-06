#!/usr/bin/env python
# coding: utf-8
"""
    tests.test_core_itertools
    ~~~~~~~~~~~~~~~~~~~~~~~~
    pyextend.core.itertools  test case

    :copyright: (c) 2016 by Vito.
    :license: GNU, see LICENSE for more details.
"""
import pytest

def test_json2csv():
    from pyextend.core.json2csv import json2csv

    source = [
        '{"dbm": 0, "created": "2016-03-21 08:07:11", "registered": false, "lat": 30.303772000000002, "radio": "LTE", '
        '"key": "1cc0000000058b304cf3881", "provider": "network", "imei": "867323022973331", "lng": 120.31240999999997}',
        '{"dbm": 0, "created": "2016-03-04 06:00:46", "registered": false, "lat": 30.259325583333339, "radio": "LTE",'
        ' "key": "1cc00000000681e0b0c5a06", "provider": "network", "imei": "867831028141570", "lng": 120.19723466666666}',
        '{"dbm": 0, "created": "2016-03-08 07:50:40", "registered": false, "lat": 28.959314250000002, "radio": "LTE",'
        ' "key": "1cc0000000057090bc0ea02", "provider": "network", "imei": "869634022225904", "lng": 118.88883787500001}',
    ]

    for line in source:
        print json2csv(line)


if __name__ == '__main__':
    pytest.main(__file__)
