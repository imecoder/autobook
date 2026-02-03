import json

with open('ethiopian_airlines_routes.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

dest_set = set()
for city in data['cities']:
    for region in ['africa', 'europe', 'asia', 'middle_east', 'americas', 'other']:
        dest_set.update(city['destinations'].get(region, []))

print('Total unique destinations:', len(dest_set))
print('Destinations:')
for dest in sorted(dest_set):
    print(dest)

# Load CITY_IATA
with open('city_iata.py', 'r', encoding='utf-8') as f:
    exec(f.read())

missing = [d for d in dest_set if d not in CITY_IATA]
print('\nMissing in CITY_IATA:', len(missing))
for d in sorted(missing):
    print(d)
