#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json


def get_payload(_date, _carrier_code, _cabin, _class):
    data = {
        "currencyCode": "NGN",
        "originDestinations": [
            {
                "id": "1",
                "originLocationCode": "LOS",
                "destinationLocationCode": "FRA",
                "departureDateTimeRange": {
                    "date": _date,
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
                        _carrier_code
                    ]
                },
                "cabinRestrictions": [
                    {
                        "cabin": _cabin,
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
            "class": _class,
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
