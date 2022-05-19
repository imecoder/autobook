#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json


def get_payload():
    data = {
        "currencyCode": "NGN",
        "originDestinations": [
            {
                "id": "1",
                "originLocationCode": "LOS",
                "destinationLocationCode": "FRA",
                "departureDateTimeRange": {
                    "date": "2022-05-31",
                    "dateWindow": "I1D"
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
            }
        ],
        "sources": [
            "GDS"
        ],
        "searchCriteria": {
            "maxFlightOffers": 1,
            "flightFilters": {
                "carrierRestrictions": {
                    "includedCarrierCodes": [
                        "LH"
                    ]
                },
                "cabinRestrictions": [
                    {
                        "cabin": "ECONOMY",
                        "originDestinationIds": [
                            1
                        ]
                    }
                ],
                "connectionRestriction": {
                    "maxNumberOfConnections": 2,
                    "airportChangeAllowed": False,
                    "technicalStopsAllowed": True
                }
            },
            "includeClosedContent": False,
            "class": "Y",
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
