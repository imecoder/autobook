#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json


def get_payload(book_id):
    data = {
        "data": {
            "type": "flight-order",
            "id": book_id,
            "remarks": {
                "general": [
                    {
                        "subType": "GENERAL_MISCELLANEOUS",
                        "text": "Amadeus - Test Remark - this is test"
                    }
                ]
            }
        }
    }

    return data
