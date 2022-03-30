#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json

def get_payload(flight_offers):
    data = {
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
                },
                {
                    "id": "2",
                    "dateOfBirth": "1985-10-16",
                    "name": {
                        "firstName": "Jennifer",
                        "lastName": "Mustermann"
                    },
                    "gender": "FEMALE",
                    "contact": {
                        "emailAddress": "Jennifer@Mustermann.com",
                        "phones": [
                            {
                                "deviceType": "MOBILE",
                                "countryCallingCode": "33",
                                "number": "480080076"
                            }
                        ]
                    }
                },
                {
                    "id": "3",
                    "dateOfBirth": "2017-10-07",
                    "name": {
                        "firstName": "Heike",
                        "lastName": "Mustermann"
                    },
                    "gender": "FEMALE",
                    "contact": {
                        "purpose": "STANDARD_WITHOUT_TRANSMISSION",
                        "emailAddress": "Heike@Mustermann.com",
                        "phones": [
                            {
                                "deviceType": "MOBILE",
                                "countryCallingCode": "33",
                                "number": "480080077"
                            }
                        ]
                    }
                },
                {
                    "id": "4",
                    "dateOfBirth": "2020-12-07",
                    "name": {
                        "firstName": "Heinz",
                        "lastName": "Mustermann"
                    },
                    "gender": "MALE",
                    "contact": {
                        "purpose": "STANDARD_WITHOUT_TRANSMISSION",
                        "emailAddress": "Heinz@Mustermann.com",
                        "phones": [
                            {
                                "deviceType": "MOBILE",
                                "countryCallingCode": "33",
                                "number": "480080078"
                            }
                        ]
                    }
                }
            ],
            "ticketingAgreement": {
                "option": "DELAY_TO_CANCEL",
                "delay": "6D"
            }
        }
    }

    return data
