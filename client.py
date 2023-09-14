import requests

# Creating record
response = requests.post('http://127.0.0.1:5000/ad/',
                         json={'header': 'Sell goat',
                               'text': 'Nice goat - drinks beer',
                               'owner': 'Goat farm',
                               }

                         )
print(response.status_code)
print(response.json())

#Get record
response = requests.get('http://127.0.0.1:5000/ad/1',)
print(response.status_code)
print(response.json())

# Update record
response = requests.patch('http://127.0.0.1:5000/ad/1',
                          json={'header': 'Get goat for free',
                                'text': 'Drank out all my beer',
                                'owner': 'Goat farm',
                                }
                          )
print(response.status_code)
print(response.json())

# Print record
response = requests.get('http://127.0.0.1:5000/ad/1',)
print(response.status_code)
print(response.json())

#Delete record
response = requests.delete(
    "http://127.0.0.1:5000/ad/1",
)
print(response.status_code)
print(response.json())

# Checking if the record was deleted
response = requests.get(
    "http://127.0.0.1:5000/ad/1",
)
print(response.status_code)
print(response.json())
