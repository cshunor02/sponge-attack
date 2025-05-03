'''
New York Times Books/Bestsellers API
https://api.nytimes.com/svc/books/v3/lists/best-sellers/history.json?api-key=[YOUR_API_KEY]
'''

import requests
import json, time

def get_best_sellers(api_key):
    max = 10000
    limit = 100
    all_res = []
    for i in range(1000, max, 20):
        url = f"https://api.nytimes.com/svc/books/v3/lists/best-sellers/history.json?api-key={api_key}&offset={i}"
        response = requests.get(url)
        time.sleep(1)
        if response.status_code == 200:
            data = response.json()
            all_res.extend(data['results'])
        else:
            print(f"Error: {response.status_code}")
        limit -= 20
        if limit <= 0:
            time.sleep(60)
            limit = 100
    return all_res
    
def save_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    api_key = ''
    best_sellers = get_best_sellers(api_key)
    if best_sellers:
        save_to_file(best_sellers, 'inputs/books5.json')
    else:
        print("Failed to retrieve best sellers data")

if __name__ == "__main__":
    main()
