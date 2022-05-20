import pykakasi
import reverse_geocode
from pyokaka import okaka

coordinates = [35.454, 132.12],
code = reverse_geocode.search(coordinates)
print(code)
print(code[0]['city'])

print(okaka.convert(code[0]['country']))
print(okaka.convert(code[0]['city']))
print(code)