from amadeus import Client, ResponseError

amadeus = Client(
    client_id='WXIAONAN',
    client_secret='Tut@2020'
)

try:
    response = amadeus.shopping.flight_offers_search.get(
        originLocationCode='MAD',
        destinationLocationCode='ATH',
        departureDate='2022-06-01',
        adults=1)
    print(response.data)
except ResponseError as error:
    print(error)
