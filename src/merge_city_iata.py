import sys

# 读取city_iata2.py中的字典
with open('city_iata2.py', 'r', encoding='utf-8') as f:
    exec(f.read())
iata_to_city = CITY_IATA

# 颠倒
city_to_iata = {v: k for k, v in iata_to_city.items()}

# 读取city_iata.py中的字典
with open('city_iata.py', 'r', encoding='utf-8') as f:
    exec(f.read())
existing = CITY_IATA

# 合并：以existing为基础，添加city_to_iata中缺失的键
merged = existing.copy()
for city, iata in city_to_iata.items():
    if city not in merged:
        merged[city] = iata
    # 如果已存在，可以选择覆盖或不覆盖，这里选择不覆盖以保留原值

# 按城市名排序
sorted_merged = dict(sorted(merged.items(), key=lambda x: x[0]))

# 输出为Python字典格式
print('CITY_IATA = {')
for city, iata in sorted_merged.items():
    print(f'    "{city}": "{iata}",')
print('}')
