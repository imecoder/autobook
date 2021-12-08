from amadeus import Client, ResponseError
import logging



logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

amadeus = Client(
    client_id='te8ZC3BmobVE8DYpJck8s1Isvx73FZ7m',
    client_secret='SkdB6l1jU1UK7j0Z',
    logger=logger
)
try:
    '''
    Retrieve the seat map of a flight present in an order
    '''
    response = amadeus.shopping.seatmaps.get(flightorderId='eJzTd9cPDPMwcooAAAtXAmE=')
    print(response.data)
except ResponseError as error:
    raise error