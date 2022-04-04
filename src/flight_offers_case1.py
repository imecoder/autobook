#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json

def get_payload():
    data = {
        "currencyCode": "GBP",
        "originDestinations": [
            {
                "id": "1",
                "originLocationCode": "LOS",
                "destinationLocationCode": "AMS",
                "departureDateTimeRange": {
                    "date": "2022-04-10",
                    "dateWindow": "I3D"
                }
            },
            {
                "id": "2",
                "originLocationCode": "AMS",
                "destinationLocationCode": "LOS",
                "departureDateTimeRange": {
                    "date": "2022-04-14",
                    "dateWindow": "I3D"
                }
            }
        ],
        "travelers": [
            {
                "id": "1",
                "travelerType": "ADULT",
                "fareOptions": [
                    "STANDARD"
                ]
            },
            {
                "id": "2",
                "travelerType": "ADULT",
                "fareOptions": [
                    "STANDARD"
                ]
            },
            {
                "id": "3",
                "travelerType": "CHILD",
                "fareOptions": [
                    "STANDARD"
                ]
            },
            {
                "id": "4",
                "travelerType": "HELD_INFANT",
                "fareOptions": [
                    "STANDARD"
                ],
                "associatedAdultId": "1"
            }
        ],
        "sources": [
            "GDS"
        ],
        "searchCriteria": {
            "maxFlightOffers": 1,
            "pricingOptions": {
                "fareType": [
                    "PUBLISHED"
                ],
                "includedCheckedBagsOnly": False
            },
            "additionalInformation": {
                "chargeableCheckedBags": False,
                "brandedFares": True
            }
        }
    }

    return data
