#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import json
import time
import pandas as pd
from datetime import datetime

from mylog import logger
import mynet
import myfile
import data_search

import requests
import os
from openpyxl import load_workbook

def do_get_token(session):
    """Get Amadeus API access token."""
    url_token = 'https://travel.api.amadeus.com/v1/security/oauth2/token'

    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
    }

    payload = "grant_type=client_credentials&client_id=IhVSuf2u1CImHOwSGCpBCkxLlZvJd07b&client_secret=GS2y32UKgJqEgUQS"

    ret, response = mynet.post(session=session, url=url_token, headers=headers, payload=payload)
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, ''

    try:
        access_token = json.loads(response.text)['access_token']
    except json.decoder.JSONDecodeError as e:
        logger.warning('解析json失败 : ' + str(e))
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, ''

    logger.warning('access_token = ' + access_token)
    return True, access_token


def do_search(session, access_token, ama_client_ref, payload):
    """Perform flight search."""
    url = 'https://travel.api.amadeus.com/v2/shopping/flight-offers'

    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + access_token,
        'ama-client-ref': ama_client_ref
    }

    ret, response = mynet.post(session=session, url=url, headers=headers, payload=json.dumps(payload))
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, {}

    try:
        jsonResponse = json.loads(response.text)

        if 'errors' in jsonResponse:
            if jsonResponse["errors"]['title'] == 'Access token expired':
                return False, '38192'
            logger.warning(response.text)
            logger.warning('查询失败，请检查查询条件')
            return False, ''

        if 'meta' not in jsonResponse:
            logger.warning('查询失败，请检查查询条件')
            return False, ''

        count = jsonResponse["meta"]["count"]
        if count == 0:
            logger.warning('没有查询到匹配的航班')
            return False, ''

        search_result = jsonResponse['data'][0]
    except json.decoder.JSONDecodeError as e:
        logger.warning('解析json失败 : ' + str(e))
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, ''

    return True, search_result


def extract_flight_info(search_result, currency, prefix=None):
    """
    Extract relevant flight information from search and pricing results.
    If prefix is provided, keys will be prefixed with prefix + '_'.
    Returns a dict with flight details and price info.
    """
    # Basic info from search result
    itineraries = search_result.get('itineraries', [])
    segments = []
    cabin_classes = []  # Store cabin class for each segment
    booking_classes = []  # Store booking class for each segment
    
    for itin in itineraries:
        for seg in itin.get('segments', []):
            segments.append({
                'departure_airport': seg['departure']['iataCode'],
                'arrival_airport': seg['arrival']['iataCode'],
                'departure_time': seg['departure']['at'],
                'arrival_time': seg['arrival']['at'],
                'carrier': seg['carrierCode'],
                'flight_number': seg['number'],
                'aircraft': seg.get('aircraft', {}).get('code', ''),
                'duration': seg.get('duration', ''),
            })
    
    # Extract cabin and booking class from pricing result
    traveler_pricings = search_result.get('travelerPricings', [])
    if traveler_pricings:
        fare_details_by_segment = traveler_pricings[0].get('fareDetailsBySegment', [])
        for i, fare_detail in enumerate(fare_details_by_segment):
            cabin = fare_detail.get('cabin', '')
            booking_class = fare_detail.get('class', '')
            cabin_classes.append(cabin)
            booking_classes.append(booking_class)
    
    # Price info
    price_info = search_result.get('price', {})
    total = price_info.get('total', '0')
    base = price_info.get('base', '0')
    currency = price_info.get('currency', currency)

    # Construct a summary row
    row = {}
    if prefix:
        row[f'{prefix}_total_price'] = total
        row[f'{prefix}_base_price'] = base
    else:
        row['total_price'] = total
        row['base_price'] = base
        # Include segment info only when no prefix (legacy)
        row['segments_count'] = len(segments)
        row['first_departure'] = segments[0]['departure_time'] if segments else ''
        row['first_arrival'] = segments[0]['arrival_time'] if segments else ''
        # Generate flight numbers as "carrier+flight_number" e.g., "ET501, ET502"
        flight_numbers_list = [f"{s['carrier']}{s['flight_number']}" for s in segments]
        row['flight_numbers'] = ', '.join(flight_numbers_list)
        # Store cabin and booking class
        if cabin_classes:
            row['cabin'] = ', '.join(cabin_classes)
        if booking_classes:
            row['booking_class'] = ', '.join(booking_classes)
    return row, segments, cabin_classes, booking_classes


def get_exchange_rate(base_currency, target_currency):
    """
    Get exchange rate from base_currency to target_currency.
    Uses free API from exchangerate-api.com.
    Returns rate (float) or None if failed.
    """
    import requests
    try:
        # Try exchangerate-api.com free endpoint
        url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            rate = data['rates'].get(target_currency)
            if rate:
                print(f"汇率获取成功: 1 {base_currency} = {rate} {target_currency}")
                return float(rate)
        
        # Fallback: try fixer.io (requires API key but free tier available)
        # For simplicity, we'll just return None if first attempt fails
        print(f"警告: 无法从API获取 {base_currency} 到 {target_currency} 的汇率")
        return None
    except Exception as e:
        print(f"获取汇率时出错: {e}")
        return None


def load_airlines_config():
    """Load configuration from airlines.json."""
    with open('airlines.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def list_cities():
    """Load city list from airlines.json."""
    data = load_airlines_config()
    cities = [city['name'] for city in data['cities']]
    return cities


def get_date_and_city_pairs():
    """Load date and all city pairs from airlines.json."""
    data = load_airlines_config()
    date = data.get('date', '2026-02-20')  # default if missing
    carriers = data.get('carriers', [])
    first_currency = data.get('first_currency', 'CNY')
    second_currency = data.get('second_currency', 'USD')
    cities = data['cities']
    # Load CITY_IATA mapping
    from city_iata import CITY_IATA
    pairs = []
    for city in cities:
        origin = city['name']
        destinations = []
        for region in ['africa', 'europe', 'asia', 'middle_east', 'americas', 'other']:
            destinations.extend(city['destinations'].get(region, []))
        # deduplicate
        destinations = list(set(destinations))
        for dest in destinations:
            # Only include if both origin and destination are in CITY_IATA
            if origin in CITY_IATA and dest in CITY_IATA:
                pairs.append((origin, dest))
            else:
                # Log missing cities (optional)
                if origin not in CITY_IATA:
                    print(f"警告: 源城市 '{origin}' 不在 CITY_IATA 映射中，跳过。")
                if dest not in CITY_IATA:
                    print(f"警告: 目的城市 '{dest}' 不在 CITY_IATA 映射中，跳过。")
    return date, carriers, first_currency, second_currency, pairs


def get_city_pairs_with_date(date):
    """Load city pairs from airlines.json for a given date."""
    data = load_airlines_config()
    cities = data['cities']
    # Load CITY_IATA mapping
    from city_iata import CITY_IATA
    pairs = []
    for city in cities:
        origin = city['name']
        destinations = []
        for region in ['africa', 'europe', 'asia', 'middle_east', 'americas', 'other']:
            destinations.extend(city['destinations'].get(region, []))
        # deduplicate
        destinations = list(set(destinations))
        for dest in destinations:
            # Only include if both origin and destination are in CITY_IATA
            if origin in CITY_IATA and dest in CITY_IATA:
                pairs.append((origin, dest))
            else:
                # Log missing cities (optional)
                if origin not in CITY_IATA:
                    print(f"警告: 源城市 '{origin}' 不在 CITY_IATA 映射中，跳过。")
                if dest not in CITY_IATA:
                    print(f"警告: 目的城市 '{dest}' 不在 CITY_IATA 映射中，跳过。")
    return pairs


def main():
    
    # 从 airlines.json 加载配置
    print("正在加载 airlines.json 配置...")
    date, carriers, first_currency, second_currency, city_pairs = get_date_and_city_pairs()
    print(f"使用日期: {date}")
    print(f"航司列表: {carriers}")
    print(f"第一货币: {first_currency}")
    print(f"第二货币: {second_currency}")
    print(f"找到 {len(city_pairs)} 个城市对需要查询。")

    # 获取汇率（从第二货币到第一货币）- 根据用户要求互换第一第二货币
    print(f"正在从API获取汇率 {second_currency} -> {first_currency}...")
    exchange_rate = get_exchange_rate(second_currency, first_currency)
    if exchange_rate is None:
        print(f"警告: 无法获取汇率，使用默认值 1 {second_currency} = 7.14 {first_currency}")
        exchange_rate = 7.14  # 默认值 (1 USD ≈ 7.14 CNY)
    else:
        print(f"使用汇率: 1 {second_currency} = {exchange_rate} {first_currency}")

    session = requests.session()

    # 获取令牌
    ret, access_token = do_get_token(session)
    if not ret:
        print("无法获取访问令牌。")
        return

    # 准备输出文件名
    filename = f"flight_prices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    print(f"输出文件: {filename}")

    # 准备货币列表
    currencies = [first_currency, second_currency]
    total_city_pairs = len(city_pairs)
    total_carriers = len(carriers)

    # 定义列顺序
    flight_info_columns = ['origin', 'destination', 'segments_count',
                          'first_departure', 'first_arrival', 'carrier', 'flight_numbers',
                          'cabin', 'booking_class']

    # 遍历每个城市对
    for idx, (origin_city, destination_city) in enumerate(city_pairs, 1):
        print(f"[{idx}/{total_city_pairs}] 查询航班: {origin_city} -> {destination_city}")

        # 遍历每个航司
        for carrier in carriers:
            print(f"  航司 {carrier}...")
            combined_row = {}
            segments = None

            # 处理每种货币
            for currency in currencies:
                print(f"    货币 {currency}...")
                ama_client_ref = 'LOSN828UU-' + str(time.time())

                # 获取 payload，注意参数顺序：origin_city, destination_city, date, carrier, currency
                try:
                    payload = data_search.get_payload(origin_city, destination_city, date, carrier, currency)
                except ValueError as e:
                    print(f"      错误: {e}")
                    continue

                # 搜索
                ret, search_result = do_search(session, access_token, ama_client_ref, payload)
                if not ret:
                    print(f"      搜索失败，货币 {currency}。")
                    continue

                # 提取信息，使用前缀
                prefix = currency.lower()  # 例如 'cny' 或 'usd'
                row, seg, cabin_classes, booking_classes = extract_flight_info(search_result, currency, prefix=prefix)
                # 合并到 combined_row
                combined_row.update(row)
                # 保留第一个成功货币的 segments（应该相同）
                if segments is None:
                    segments = seg
                # 存储舱位和预订等级信息（仅一次，从第一个货币）
                if cabin_classes and 'cabin' not in combined_row:
                    combined_row['cabin'] = ', '.join(cabin_classes)
                if booking_classes and 'booking_class' not in combined_row:
                    combined_row['booking_class'] = ', '.join(booking_classes)

            # 如果没有货币成功，跳过
            if not combined_row:
                print(f"      未获取到任何货币的数据，跳过。")
                continue

            # 添加公共字段（航班信息）
            from city_iata import CITY_IATA
            combined_row['origin'] = CITY_IATA.get(origin_city)
            combined_row['destination'] = CITY_IATA.get(destination_city)
            if segments:
                combined_row['segments_count'] = len(segments)
                combined_row['first_departure'] = segments[0]['departure_time'] if segments else ''
                combined_row['first_arrival'] = segments[0]['arrival_time'] if segments else ''
                combined_row['carrier'] = carrier
                # 生成航班号列表
                flight_numbers_list = [f"{s['carrier']}{s['flight_number']}" for s in segments]
                combined_row['flight_numbers'] = ', '.join(flight_numbers_list)

            # 计算对比字段
            try:
                # 获取价格（字符串转换为浮点数）
                first_base = float(combined_row.get(f'{first_currency.lower()}_base_price', 0))
                first_total = float(combined_row.get(f'{first_currency.lower()}_total_price', 0))
                second_base = float(combined_row.get(f'{second_currency.lower()}_base_price', 0))
                second_total = float(combined_row.get(f'{second_currency.lower()}_total_price', 0))

                # 使用汇率将第二货币价格转换为第一货币
                # 注意：exchange_rate 现在是 1 second = X first，所以使用乘法
                if exchange_rate != 0:
                    second_total_in_first = second_total * exchange_rate
                    second_base_in_first = second_base * exchange_rate
                else:
                    second_total_in_first = 0.0
                    second_base_in_first = 0.0

                # 计算价格差异
                total_price_diff = first_total - second_total_in_first
                base_price_diff = first_base - second_base_in_first

                # 计算百分比差异
                if first_total != 0:
                    total_price_diff_pct = (total_price_diff / first_total) * 100
                else:
                    total_price_diff_pct = 0.0

                if first_base != 0:
                    base_price_diff_pct = (base_price_diff / first_base) * 100
                else:
                    base_price_diff_pct = 0.0

                # 添加对比字段
                combined_row[f'{second_currency.lower()}:{first_currency.lower()}_rate'] = exchange_rate
                combined_row[f'{second_currency.lower()}_total_in_{first_currency.lower()}'] = second_total_in_first
                combined_row[f'{second_currency.lower()}_base_in_{first_currency.lower()}'] = second_base_in_first
                combined_row['total_price_diff'] = total_price_diff
                combined_row['total_price_diff_pct'] = total_price_diff_pct
                combined_row['base_price_diff'] = base_price_diff
                combined_row['base_price_diff_pct'] = base_price_diff_pct

                # 确定哪个货币更便宜
                if total_price_diff > 0:
                    combined_row['cheaper_currency'] = second_currency
                    combined_row['cheaper_amount'] = total_price_diff
                elif total_price_diff < 0:
                    combined_row['cheaper_currency'] = first_currency
                    combined_row['cheaper_amount'] = -total_price_diff
                else:
                    combined_row['cheaper_currency'] = 'equal'
                    combined_row['cheaper_amount'] = 0.0

            except (KeyError, ValueError, TypeError) as e:
                # 如果任何必需字段缺失，设置默认值
                print(f"    警告: 计算对比字段时出错: {e}")
                combined_row[f'{second_currency.lower()}:{first_currency.lower()}_rate'] = exchange_rate
                combined_row[f'{second_currency.lower()}_total_in_{first_currency.lower()}'] = 0.0
                combined_row[f'{second_currency.lower()}_base_in_{first_currency.lower()}'] = 0.0
                combined_row['total_price_diff'] = 0.0
                combined_row['total_price_diff_pct'] = 0.0
                combined_row['base_price_diff'] = 0.0
                combined_row['base_price_diff_pct'] = 0.0
                combined_row['cheaper_currency'] = 'unknown'
                combined_row['cheaper_amount'] = 0.0

            # 重新排列列顺序：航班信息、价格、对比
            ordered_row = {}

            # 1. 航班信息列
            for col in flight_info_columns:
                if col in combined_row:
                    ordered_row[col] = combined_row[col]

            # 2. 价格列（第一货币然后第二货币）
            price_columns = []
            for currency in currencies:
                code = currency.lower()
                price_columns.extend([f'{code}_base_price', f'{code}_total_price'])

            for col in price_columns:
                if col in combined_row:
                    ordered_row[col] = combined_row[col]

            # 3. 对比列
            comparison_columns = [
                f'{second_currency.lower()}:{first_currency.lower()}_rate',
                f'{second_currency.lower()}_total_in_{first_currency.lower()}',
                f'{second_currency.lower()}_base_in_{first_currency.lower()}',
                'total_price_diff',
                'total_price_diff_pct',
                'base_price_diff',
                'base_price_diff_pct',
                'cheaper_currency',
                'cheaper_amount'
            ]

            for col in comparison_columns:
                if col in combined_row:
                    ordered_row[col] = combined_row[col]

            # 将行追加到 Excel
            df_row = pd.DataFrame([ordered_row])
            # 如果文件不存在，写入表头，否则追加无表头
            if not os.path.exists(filename):
                df_row.to_excel(filename, index=False)
            else:
                # 加载现有工作簿并追加行
                with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                    # 读取现有工作表以确定起始行
                    try:
                        existing_df = pd.read_excel(filename, sheet_name=0)
                        startrow = len(existing_df) + 1
                    except Exception:
                        startrow = 1
                    df_row.to_excel(writer, index=False, header=False, startrow=startrow)
            print(f"    已写入一行数据到 {filename}")

    # 最终总结
    if os.path.exists(filename):
        df = pd.read_excel(filename)
        print(f"总共获取了 {len(df)} 条记录。")
        print("列顺序:", list(df.columns))
    else:
        print("未获得任何结果。")



if __name__ == '__main__':
    main()
