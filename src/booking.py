#!/usr/bin/python
import sys

import requests
import json
import time

from mylog import *
import myfile
import mynet
import mylimit

session = requests.session()

ret, base_config = myfile.read_json('config.base.json')
if ret == False:
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
		access_token = json.loads(response.text)['access_token']
	except json.decoder.JSONDecodeError as e:
		logger.warning('解析json失败 : ' + str(e))
		logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
		return False, ''

	logger.warning('access_token = ' + access_token)

	return True, access_token


def do_search(access_token, ama_client_ref, payload) :

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

		if 'errors' in jsonResponse :
			if jsonResponse["errors"]['code'] == 38192 :
				return False, '38192'

		if 'meta' not in jsonResponse:
			logger.warning('查询失败，请检查查询条件')
			return False, ''

		count = jsonResponse["meta"]["count"]
		if count==0 :
			logger.warning('没有查询到匹配的航班')
			return False,''

		search_result = jsonResponse['data'][0]
	except json.decoder.JSONDecodeError as e:
		logger.warning('解析json失败 : ' + str(e))
		logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
		return False, ''

	return True, search_result


def do_price(access_token, ama_client_ref, search_result) :

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
		return False

	try:
		jsonResponse = json.loads(response.text)

		if 'errors' in jsonResponse :
			if jsonResponse["errors"]['code'] == 38192 :
				return False, '38192'

		if json.loads(response.text)["data"]["type"] != "flight-offers-pricing" :
			logger.warning('查询价格错误')
			return False, ''
	except json.decoder.JSONDecodeError as e:
		logger.warning('解析json失败 : ' + str(e))
		logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
		return False, ''

	return True, ''



def do_order(access_token, ama_client_ref, payload) :

	url = 'https://travel.api.amadeus.com/v1/booking/flight-orders'

	headers = {
		'Content-Type': "application/json",
		'Authorization': "Bearer " + access_token ,
		'ama-client-ref': ama_client_ref
	}

	ret, response = mynet.post(session=session, url=url, headers=headers, payload=json.dumps(payload))
	if ret == False:
		logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
		return False, ""


	try:
		jsonResponse = json.loads(response.text)

		if 'errors' in jsonResponse :
			if jsonResponse["errors"]['code'] == 38192 :
				return False, '38192'

		PNR = jsonResponse["data"]["associatedRecords"][0]["reference"]
		logger.warning('PNR = ' + PNR)
		return True, PNR

	except json.decoder.JSONDecodeError as e:
		logger.warning('解析json失败 : ' + str(e))
		logger.warning(sys._getframe().f_code.co_name + ' 运行失败')
		return False, ''


	return True, PNR



def main():
	branch_size = base_config['branch_size']
	print(branch_size)

	while True :
		if mylimit.limit() == True:
			exit(0)

		ret, access_token = do_get_token()
		if ret == False :
			time.sleep(5)
			continue

		while True:
			ama_client_ref = 'LOSN828UU-' + str(time.time())

			# 获取查询配置
			import data_search
			payload = data_search.get_payload()

			# 调用查找
			ret, search_result = do_search(access_token, ama_client_ref, payload)
			if ret == False :
				if search_result == '38192' :
					break
				continue

			# 查价格
			ret, price_result = do_price(access_token, ama_client_ref, search_result)
			if ret == False :
				if price_result == '38192' :
					break
				continue

			# 获取制作订单信息
			import data_order
			payload = data_order.get_payload(search_result)

			# 订票
			ret, PNR = do_order(access_token, ama_client_ref, payload)
			if ret == False :
				if PNR == '38192' :
					break
				continue

			# 此时订票成功已经成功的情况下
			break

		# 此时订票成功已经成功的情况下
		break

	logger.warning('程序退出 ...')
	logger.warning('')
	logger.warning('')


if __name__ == '__main__':
	main()
