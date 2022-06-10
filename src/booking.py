#!/usr/bin/python
import sys

import requests
import json
import time

from myflag import *
from mylog import *
import myfile
import mynet
import mylimit

from threading import Thread

session = requests.session()

ret, book_config = myfile.read_json("config.book.json")
if ret == False :
    exit(0)


def do_get_token() :
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
		_token = json.loads(response.text)['access_token']
	except json.decoder.JSONDecodeError as e:
		logger.warning('解析json失败 : ' + str(e))
		logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
		return False, ''

	logger.warning('token = ' + _token)

	return True, _token


def do_search(_token, ama_client_ref, payload) :

	url = 'https://travel.api.amadeus.com/v2/shopping/flight-offers'

	headers = {
		'Content-Type': "application/json",
		'Authorization': "Bearer " + _token,
		'ama-client-ref': ama_client_ref
	}

	ret, response = mynet.post(session=session, url=url, headers=headers, payload=json.dumps(payload))
	if ret == False:
		logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
		return False, {}

	try:
		jsonResponse = json.loads(response.text)

		if 'errors' in jsonResponse :
			if 'Access token expired' in jsonResponse["errors"][0]['title'] :
				return False, '38192'
			logger.warning(response.text)
			logger.warning('查询失败，请检查查询条件')
			return False, ''

		if 'meta' not in jsonResponse:
			logger.warning('查询失败，请检查查询条件')
			return False, ''

		count = jsonResponse["meta"]["count"]
		if count==0 :
			logger.warning('没有查询到匹配的航班')
			return False,''

	except json.decoder.JSONDecodeError as e:
		logger.warning('解析json失败 : ' + str(e))
		logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
		return False, ''

	return True, jsonResponse['data']


def do_filter(_search_result, _date, _carrier_code, _cabin, _class) :

	for _flight in _search_result :

		if _date not in _flight['itineraries'][0]['segments'][0]['departure']['at'] and \
				_date not in _flight['itineraries'][0]['segments'][0]['arrival']['at'] :
			continue

		if len(_flight['itineraries'][0]['segments']) == 0 :
			if _carrier_code != _flight['itineraries'][0]['segments'][0]['operating']['carrierCode'] :
				continue
		else :
			if _carrier_code != _flight['itineraries'][0]['segments'][0]['operating']['carrierCode'] and \
					_carrier_code != _flight['itineraries'][0]['segments'][1]['operating']['carrierCode'] :
				continue


		if len(_flight['travelerPricings'][0]['fareDetailsBySegment']) == 0 :
			if _cabin != _flight['travelerPricings'][0]['fareDetailsBySegment'][0]['cabin'] :
				continue

			if _class != _flight['travelerPricings'][0]['fareDetailsBySegment'][0]['class']:
				continue
		else :
			if _cabin != _flight['travelerPricings'][0]['fareDetailsBySegment'][0]['cabin'] and \
					_cabin != _flight['travelerPricings'][0]['fareDetailsBySegment'][1]['cabin'] :
				continue

			if _class != _flight['travelerPricings'][0]['fareDetailsBySegment'][0]['class'] and \
					_class != _flight['travelerPricings'][0]['fareDetailsBySegment'][1]['class'] :
				continue


		return True, _flight

	return False,''


def do_price(_token, ama_client_ref, search_result) :

	url = 'https://travel.api.amadeus.com/v1/shopping/flight-offers/pricing'

	headers = {
		'Content-Type': "application/json",
		'Authorization': "Bearer " + _token,
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
		return False

	try:
		jsonResponse = json.loads(response.text)

		if 'errors' in jsonResponse :
			if 'Access token expired' in jsonResponse["errors"][0]['title'] :
				return False, '38192'
			logger.warning(response.text)
			return False, ''

		if json.loads(response.text)["data"]["type"] != "flight-offers-pricing" :
			logger.warning('查询价格错误')
			return False, ''
	except json.decoder.JSONDecodeError as e:
		logger.warning('解析json失败 : ' + str(e))
		logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
		return False, ''

	return True, ''



def do_order(_token, ama_client_ref, payload) :

	url = 'https://travel.api.amadeus.com/v1/booking/flight-orders'

	headers = {
		'Content-Type': "application/json",
		'Authorization': "Bearer " + _token ,
		'ama-client-ref': ama_client_ref
	}

	ret, response = mynet.post(session=session, url=url, headers=headers, payload=json.dumps(payload))
	if ret == False:
		logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
		return False, ""


	try:
		jsonResponse = json.loads(response.text)

		if 'errors' in jsonResponse :
			if 'Access token expired' in jsonResponse["errors"][0]['title'] :
				return False, '38192'
			logger.warning(response.text)
			return False, ''

		PNR = jsonResponse["data"]["associatedRecords"][0]["reference"]
		logger.warning('PNR = ' + PNR)
		return True, PNR

	except json.decoder.JSONDecodeError as e:
		logger.warning('解析json失败 : ' + str(e))
		logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
		return False, ''


	return True, PNR


def process(_date, _carrier_code, _cabin, _class) :

	while True :
		if mylimit.limit() == True:
			exit(0)

		if is_occupied_over() :
			logger.warning("已占票, 当前分支退出.")
			return

		ret, _token = do_get_token()
		if ret == False :
			time.sleep(5)
			continue

		###################
		continue

		while True:
			ama_client_ref = 'LOSN828UU-' + str(time.time())

			# 获取查询配置
			import data_search
			payload = data_search.get_payload(_date, _carrier_code)

			if is_occupied_over():
				logger.warning("已占票, 当前分支退出.")
				return

			# 调用查找
			ret, search_result = do_search(_token, ama_client_ref, payload)
			if ret == False :
				if search_result == '38192' :
					break
				continue

			###################
			continue

			if is_occupied_over():
				logger.warning("已占票, 当前分支退出.")
				return

			# 过滤
			ret, filter_result = do_filter(search_result, _date, _carrier_code, _cabin, _class)
			if ret == False :
				continue

			# 查价格
			ret, price_result = do_price(_token, ama_client_ref, filter_result)
			if ret == False :
				if price_result == '38192' :
					break
				continue

			if is_occupied_over():
				logger.warning("已占票, 当前分支退出.")
				return

			# 获取制作订单信息
			import data_order
			payload = data_order.get_payload(filter_result)

			# 订票
			ret, PNR = do_order(_token, ama_client_ref, payload)
			if ret == False :
				if PNR == '38192' :
					break

				if is_occupied_over():
					logger.warning("已占票, 当前分支退出.")
					return

				continue

			occupied_append()

			# 此时订票成功已经成功的情况下
			break

		# 此时订票成功已经成功的情况下
		break



def main():

	set_condition(book_config['need_count'])
	dates_list = book_config['dates']
	_carrier_code = book_config['carrier_code']
	_cabin = book_config['cabin']
	_class = book_config['class']
	thread_list = []

	for _date in dates_list:
		print(_date)
		t = Thread(target=process, args=(_date, _carrier_code, _cabin, _class))
		t.daemon = True
		t.name = _date
		t.start()
		thread_list.append(t)

	for t in thread_list :
		logger.warning('等待线程' + t.name + "退出中 ...")
		t.join()

	logger.warning('程序退出 ...')
	logger.warning('')
	logger.warning('')

if __name__ == '__main__':
	main()
