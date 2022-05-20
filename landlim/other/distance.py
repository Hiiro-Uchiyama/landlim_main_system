from geopy.distance import great_circle

# (緯度, 経度)
TokyoStation = (35.681382, 139.76608399999998)
YurakuchoStation = (35.675069, 139.763328)
NagoyaStation = (35.170915, 136.881537)
RiodeJaneiro = (-22.906847, -43.172897)

# WGS84モデル
dis1 = great_circle(TokyoStation, YurakuchoStation).m
# > Wall time: 41 µs
dis2 = great_circle(TokyoStation, NagoyaStation).km
# > Wall time: 52 µs
dis3 = great_circle(TokyoStation, RiodeJaneiro).km
# > Wall time: 30 µs

print(dis1)
# 744.8062679029077
print(dis2)
# 267.44664972375193
print(dis3)
# 18566.566790738878