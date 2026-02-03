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


def do_price(session, access_token, ama_client_ref, search_result):
    """Price the flight offer."""
    url = 'https://travel.api.amadeus.com/v1/shopping/flight-offers/pricing'

    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + access_token,
        'ama-client-ref': ama_client_ref
    }

    payload = {
        "data": {
            "type": "flight-offers-pricing",
            "flightOffers": [
                search_result
            ]
        }
    }

    ret, response = mynet.post(session=session, url=url, headers=headers, payload=json.dumps(payload))
    if ret == False:
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, ''

    try:
        jsonResponse = json.loads(response.text)

        if 'errors' in jsonResponse:
            if jsonResponse["errors"]['title'] == 'Access token expired':
                return False, '38192'
            logger.warning(response.text)
            return False, ''

        if json.loads(response.text)["data"]["type"] != "flight-offers-pricing":
            logger.warning('查询价格错误')
            return False, ''
    except json.decoder.JSONDecodeError as e:
        logger.warning('解析json失败 : ' + str(e))
        logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
        return False, ''

    return True, jsonResponse


def extract_flight_info(search_result, pricing_result, currency):
    """Extract relevant flight information from search and pricing results."""
    # Basic info from search result
    itineraries = search_result.get('itineraries', [])
    segments = []
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
    # Price info
    price_info = search_result.get('price', {})
    total = price_info.get('total', '0')
    base = price_info.get('base', '0')
    currency = price_info.get('currency', currency)

    # Pricing details (taxes) from pricing result if available
    taxes = []
    if pricing_result and 'data' in pricing_result:
        traveler_pricings = pricing_result['data'].get('flightOffers', [{}])[0].get('travelerPricings', [])
        if traveler_pricings:
            taxes = traveler_pricings[0].get('price', {}).get('taxes', [])

    # Construct a summary row
    row = {
        'currency': currency,
        'total_price': total,
        'base_price': base,
        'taxes': json.dumps(taxes),
        'segments_count': len(segments),
        'first_departure': segments[0]['departure_time'] if segments else '',
        'first_arrival': segments[0]['arrival_time'] if segments else '',
        'carriers': ', '.join(set(s['carrier'] for s in segments)),
        'flight_numbers': ', '.join(s['flight_number'] for s in segments),
    }
    return row


def list_cities():
    """Load city list from ethiopian_airlines_routes.json."""
    with open('ethiopian_airlines_routes.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    cities = [city['name'] for city in data['cities']]
    return cities


def get_date_and_city_pairs():
    """Load date and all city pairs from ethiopian_airlines_routes.json."""
    with open('ethiopian_airlines_routes.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    date = data.get('date', '2026-02-20')  # default if missing
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
    return date, pairs


def main():
    import requests
    session = requests.session()

    # Load date and city pairs
    date, city_pairs = get_date_and_city_pairs()
    print(f"使用日期: {date}")
    print(f"找到 {len(city_pairs)} 个城市对需要查询。")

    # Get token
    ret, access_token = do_get_token(session)
    if not ret:
        print("无法获取访问令牌。")
        return

    # Prepare currencies
    currencies = ["CNY", "USD"]
    results = []
    total_pairs = len(city_pairs)
    for idx, (origin_city, destination_city) in enumerate(city_pairs, 1):
        print(f"[{idx}/{total_pairs}] 查询航班: {origin_city} -> {destination_city}")
        for currency in currencies:
            print(f"  货币 {currency}...")
            ama_client_ref = 'LOSN828UU-' + str(time.time())

            # Get payload
            try:
                payload = data_search.get_payload_custom(origin_city, destination_city, date, currency)
            except ValueError as e:
                print(f"  错误: {e}")
                continue

            # Search
            ret, search_result = do_search(session, access_token, ama_client_ref, payload)
            if not ret:
                print(f"  搜索失败，货币 {currency}。")
                continue

            # Price
            ret, pricing_result = do_price(session, access_token, ama_client_ref, search_result)
            if not ret:
                print(f"  定价失败，货币 {currency}。")
                pricing_result = None

            # Extract info
            row = extract_flight_info(search_result, pricing_result, currency)
            row['origin'] = origin_city
            row['destination'] = destination_city
            row['date'] = date
            results.append(row)

    if not results:
        print("未获得任何结果。")
        return

    # Create DataFrame and save to Excel
    df = pd.DataFrame(results)
    filename = f"flight_prices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(filename, index=False)
    print(f"结果已保存到 {filename}")
    print(df)


if __name__ == '__main__':
    main()
