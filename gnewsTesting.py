import requests

# Replace with your API key and search engine ID
api_key = 'AIzaSyBy0k0dcl4_pGkjiSooeyZYhg8IPomKbwA'
cx = 'your-search-engine-id'
query = 'tesla'

url = f'https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cx}'

response = requests.get(url)
data = response.json()

for item in data['items']:
    print(item['title'], item['link'])

a = "AIzaSyBy0k0dcl4_pGkjiSooeyZYhg8IPomKbwA"
