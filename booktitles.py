'''
New York Times Books/Bestsellers API
https://api.nytimes.com/svc/books/v3/lists/best-sellers/history.json?api-key=[YOUR_API_KEY]
'''

import requests
import json

def get_best_sellers(api_key):
    url = f"https://api.nytimes.com/svc/books/v3/lists/best-sellers/history.json?api-key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['results']
    else:
        print(f"Error: {response.status_code}")
        return None
    
def save_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    api_key = ''
    best_sellers = get_best_sellers(api_key)
    if best_sellers:
        save_to_file(best_sellers, 'inputs/books.json')
    else:
        print("Failed to retrieve best sellers data")
