#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json


def get_payload(flight_offers):
    data = \
        {
            "data": {
                "type": "flight-order",
                "flightOffers": [
                    flight_offers
                ],
                "travelers": [
                    {
                        "id": "1",
                        "dateOfBirth": "1985-10-17",
                        "name": {
                            "firstName": "Join",
                            "lastName": "Mustermann"
                        },
                        "gender": "MALE",
                        "contact": {
                            "emailAddress": "Join@Mustermann.com",
                            "phones": [
                                {
                                    "deviceType": "MOBILE",
                                    "countryCallingCode": "33",
                                    "number": "480080075"
                                }
                            ]
                        }
                    }
                ]
            }
        }

    return data
