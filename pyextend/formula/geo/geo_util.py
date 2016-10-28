#!/usr/bin/env python
# coding: utf-8


__all__ = ['get_distance']


def get_distance(lat1, lng1, lat2, lng2, ndigits=None):
    from math import radians, atan, acos, sin, cos, tan

    lat1 = float(lat1)
    lng1 = float(lng1)
    lat2 = float(lat2)
    lng2 = float(lng2)
    ra = 6378.140  # 赤道半径
    rb = 6356.755  # 极半径 （km）
    flatten = (ra - rb) / ra  # 地球偏率
    rad_lat_1 = radians(lat1)
    rad_lng_1 = radians(lng1)
    rad_lat_2 = radians(lat2)
    rad_lng_2 = radians(lng2)
    p_a = atan(rb / ra * tan(rad_lat_1))
    p_b = atan(rb / ra * tan(rad_lat_2))
    n = sin(p_a) * sin(p_b) + cos(p_a) * cos(p_b) * cos(rad_lng_1 - rad_lng_2)
    n = -1 if n < -1 else n
    n = 1 if n > 1 else n
    xx = acos(n)
    if xx == 0.0:
        return 0.0
    c1 = (sin(xx) - xx) * (sin(p_a) + sin(p_b)) ** 2 / cos(xx / 2) ** 2
    c2 = (sin(xx) + xx) * (sin(p_a) - sin(p_b)) ** 2 / sin(xx / 2) ** 2
    dr = flatten / 8 * (c1 - c2)
    distance = ra * (xx + dr)
    return round(distance * 1000, ndigits)
