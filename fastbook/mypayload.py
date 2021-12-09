#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json



def for_access_token():
    payload = "grant_type=client_credentials&client_id=te8ZC3BmobVE8DYpJck8s1Isvx73FZ7m&client_secret=SkdB6l1jU1UK7j0Z"
    return payload



def for_flight_offers_search(book_comp, book_date, book_from, book_to):
    payload = {
        "currencyCode": "USD",
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


def for_flight_offers_booking(elem, book_comp, book_date, book_from, book_to):
    payload = {
        "data": {
            "type": "flight-order",
            "flightOffers": [
                elem
            ],
            "travelers": [
                {
                    "id": "1",
                    "dateOfBirth": "1982-01-16",
                    "name": {
                        "firstName": "JORGE",
                        "lastName": "GONZALES"
                    },
                    "gender": "MALE",
                    "contact": {
                        "emailAddress": "jorge.gonzales833@telefonica.es",
                        "phones": [
                            {
                                "deviceType": "MOBILE",
                                "countryCallingCode": "34",
                                "number": "480080076"
                            }
                        ]
                    },
                    "documents": [
                        {
                            "documentType": "PASSPORT",
                            "birthPlace": "Madrid",
                            "issuanceLocation": "Madrid",
                            "issuanceDate": "2015-04-14",
                            "number": "00000000",
                            "expiryDate": "2025-04-14",
                            "issuanceCountry": "ES",
                            "validityCountry": "ES",
                            "nationality": "ES",
                            "holder": True
                        }
                    ]
                },
                {
                    "id": "2",
                    "dateOfBirth": "2012-10-11",
                    "gender": "FEMALE",
                    "contact": {
                        "emailAddress": "jorge.gonzales833@telefonica.es",
                        "phones": [
                            {
                                "deviceType": "MOBILE",
                                "countryCallingCode": "34",
                                "number": "480080076"
                            }
                        ]
                    },
                    "name": {
                        "firstName": "ADRIANA",
                        "lastName": "GONZALES"
                    }
                }
            ],
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
