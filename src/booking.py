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
			if jsonResponse["errors"]['title'] == 'Access token expired' :
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
			# 获取制作订单信息
			import data_order
			payload = data_order.get_payload()

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
