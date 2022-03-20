#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json


def for_access_token():
    payload = "grant_type=client_credentials&client_id=Ab2CK00P0ybfc6Rxdow6WGPppMnfls8C&client_secret=dBGAVWFj3lpkOegE"
    return payload


def for_Airline_Code_Lookup():
    payload = {
        "meta": {
            "count": 1,
            "links": {
                "self": "https://test.api.amadeus.com/v1/reference-data/airlines?airlineCodes=BA"
            }
        },
        "data": [
            {
                "type": "airline",
                "iataCode": "BA",
                "icaoCode": "BAW",
                "businessName": "BRITISH AIRWAYS",
                "commonName": "BRITISH A/W"
            }
        ]
    }

    return payload

def for_flight_offers_search(book_comp, book_date, book_from, book_to):
    payload = {
        "currencyCode": "NGN",
        "originDestinations": [
            {
                "id": "1",
                "originLocationCode": book_from,
                "destinationLocationCode": book_to,
                "departureDateTimeRange": {
                    "date": book_date
                }
            }
        ],
        "travelers": [
            {
                "id": "1",
                "travelerType": "ADULT"
            }
        ],
        "sources": [
            "GDS"
        ],
        "searchCriteria": {
            "maxFlightOffers": 1,
            "flightFilters": {
                "carrierRestrictions": {
                    "includedCarrierCodes": [book_comp]
                }
            }
        }
    }

    return payload

def for_flight_offers_seatmap(elem):
    payload = {
        "data": [
            elem
        ]
    }

    return payload


def for_flight_offers_booking(elem, book_travelers):
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
