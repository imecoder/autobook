from amadeus import Client, ResponseError
import logging



logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# amadeus = Client(
#     client_id='ymUeKeaKJcxW5vN2mBdFlwcfcSQ9jyDc',
#     client_secret='mU4qd7e4Ezhl4nsX',
#     logger=logger
# )

amadeus = Client(
    client_id='te8ZC3BmobVE8DYpJck8s1Isvx73FZ7m',
    client_secret='SkdB6l1jU1UK7j0Z',
    logger=logger
)

4001554280

try:
    # response = amadeus.shopping.flight_offers_search.get(
    #     originLocationCode='LOS',
    #     destinationLocationCode='FRA',
    #     departureDate='2021-12-10',
    #     adults=1)
    # response = amadeus.shopping.flight_dates.get(origin='LOS', destination='FRA')
    response = amadeus.schedule.flights.get(
        carrierCode='LH',
        flightNumber='569',
        scheduledDepartureDate='2021-12-10')
    print(response.body)  # => The raw response, as a string
    print(response.result)  # => The body parsed as JSON, if the result was parsable
    print(response.data)  # => The list of locations, extracted from the JSON
except ResponseError as error:
    print(error)