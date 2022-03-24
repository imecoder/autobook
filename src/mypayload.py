#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json


def for_access_token():
    payload = "grant_type=client_credentials&client_id=Ab2CK00P0ybfc6Rxdow6WGPppMnfls8C&client_secret=dBGAVWFj3lpkOegE"
    return payload


def for_flight_orders(elem, book_travelers):
    payload = {
        "data": {
            "type": "flight-order",
            "flightOffers": [
                elem
            ],
            "travelers": book_travelers,
            "remarks": {
                "general": [
                    {
                        "subType": "GENERAL_MISCELLANEOUS",
                        "text": "ONLINE BOOKING FROM INCREIBLE VIAJES"
                    }
                ]
            },
            "ticketingAgreement": {
                "option": "DELAY_TO_CANCEL",
                "delay": "6D"
            },
            "contacts": [
                {
                    "addresseeName": {
                        "firstName": "PABLO",
                        "lastName": "RODRIGUEZ"
                    },
                    "companyName": "INCREIBLE VIAJES",
                    "purpose": "STANDARD",
                    "phones": [
                        {
                            "deviceType": "LANDLINE",
                            "countryCallingCode": "34",
                            "number": "480080071"
                        },
                        {
                            "deviceType": "MOBILE",
                            "countryCallingCode": "33",
                            "number": "480080072"
                        }
                    ],
                    "emailAddress": "support@increibleviajes.es",
                    "address": {
                        "lines": [
                            "Calle Prado, 16"
                        ],
                        "postalCode": "28014",
                        "cityName": "Madrid",
                        "countryCode": "ES"
                    }
                }
            ]
        }
    }

    return payload
