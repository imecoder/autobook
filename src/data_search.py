#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json


def get_payload():
    """Legacy function, kept for compatibility."""
    return get_payload_custom("LOS", "FRA", "2022-05-31", "NGN")


def get_payload_custom(origin_city, destination_city, date, currency="NGN"):
    """
    Return a payload for flight search with given parameters.
    origin_city and destination_city are city names (must be mapped to IATA codes).
    """
    from city_iata import CITY_IATA

    origin_code = CITY_IATA.get(origin_city)
    destination_code = CITY_IATA.get(destination_city)
    if origin_code is None:
        raise ValueError(f"Unknown origin city: {origin_city}")
    if destination_code is None:
        raise ValueError(f"Unknown destination city: {destination_city}")

    data = {
        "currencyCode": currency,
        "originDestinations": [
            {
                "id": "1",
                "originLocationCode": origin_code,
                "destinationLocationCode": destination_code,
                "departureDateTimeRange": {
                    "date": date,
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


def get_payloads_for_currencies(origin_city, destination_city, date, currencies=("CNY", "USD")):
    """Return a list of payloads for each currency."""
    payloads = []
    for currency in currencies:
        payloads.append(get_payload_custom(origin_city, destination_city, date, currency))
    return payloads
