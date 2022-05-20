#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json


def get_payload():
    data = \
        {
            "data": {
                "type": "flight-order",
                "flightOffers": [
                    {
                        "type": "flight-offer",
                        "id": "1",
                        "source": "GDS",
                        "instantTicketingRequired": False,
                        "nonHomogeneous": False,
                        "paymentCardRequired": False,
                        "lastTicketingDate": "2022-05-30",
                        "itineraries": [
                            {
                                "segments": [
                                    {
                                        "departure": {
                                            "iataCode": "LOS",
                                            "terminal": "I",
                                            "at": "2022-05-31T23:00:00"
                                        },
                                        "arrival": {
                                            "iataCode": "FRA",
                                            "terminal": "1",
                                            "at": "2022-06-01T06:25:00"
                                        },
                                        "carrierCode": "LH",
                                        "number": "569",
                                        "aircraft": {
                                            "code": "333"
                                        },
                                        "operating": {
                                            "carrierCode": "LH"
                                        },
                                        "duration": "PT6H25M",
                                        "id": "2",
                                        "numberOfStops": 0
                                    }
                                ]
                            }
                        ],
                        "pricingOptions": {
                            "fareType": [
                                "PUBLISHED"
                            ],
                            "includedCheckedBagsOnly": True
                        },
                        "validatingAirlineCodes": [
                            "LH"
                        ],
                        "travelerPricings": [
                            {
                                "travelerId": "1",
                                "fareOption": "STANDARD",
                                "travelerType": "ADULT",
                                "fareDetailsBySegment": [
                                    {
                                        "segmentId": "2",
                                        "cabin": "BUSINESS",
                                        "fareBasis": "CNCOWNG",
                                        "brandedFare": "BUSSAVERA",
                                        "class": "C",
                                        "includedCheckedBags": {
                                            "quantity": 2
                                        }
                                    }
                                ]
                            }
                        ]
                    }
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
