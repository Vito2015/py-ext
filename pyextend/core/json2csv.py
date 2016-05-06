#!/usr/bin/env python
# coding: utf-8
import json


def json2csv(json_str, show_header=False, separator='\t'):
    """
    Format a json string to csv like.
    :param json_str: json object string
    :param show_header: can returns csv header line
    :param separator: csv column format separator
    :return: if show_header=False: a string like csv formatting;
             if show_header=True: a tuple (header, csv string)
    """
    json_obj = json.loads(json_str)
    cols = [col for col in json_obj.keys()]
    vals = [str(json_obj.get(col)) for col in cols]
    header = None
    if show_header:
        header = separator.join(cols)
    values = separator.join(vals)

    return (header, values) if show_header else values


# if __name__ == '__main__':
#     source = [
#         '{"dbm": 0, "created": "2016-03-21 08:07:11", "registered": false, "lat": 30.303772000000002, "radio": "LTE", '
#         '"key": "1cc0000000058b304cf3881", "provider": "network", "imei": "867323022973331", "lng": 120.31240999999997}',
#         '{"dbm": 0, "created": "2016-03-04 06:00:46", "registered": false, "lat": 30.259325583333339, "radio": "LTE",'
#         ' "key": "1cc00000000681e0b0c5a06", "provider": "network", "imei": "867831028141570", "lng": 120.19723466666666}',
#         '{"dbm": 0, "created": "2016-03-08 07:50:40", "registered": false, "lat": 28.959314250000002, "radio": "LTE",'
#         ' "key": "1cc0000000057090bc0ea02", "provider": "network", "imei": "869634022225904", "lng": 118.88883787500001}',
#     ]
#
#     print (json2csv(source[0], show_header=True)[0])
#     for line in source:
#         print(json2csv(line))
