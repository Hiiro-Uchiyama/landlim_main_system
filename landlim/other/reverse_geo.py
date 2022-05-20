import reverse_geocoder

coordinates = (35.564, 133.12)
location = reverse_geocoder.search(coordinates)

print('latitude:', location[0]['lat'])
print('longitude:', location[0]['lon'])
print('longitude:', location[0]['name'])

print(location)
