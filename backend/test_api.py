import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OMDB_API_KEY')
print(f'API Key loaded: {api_key}')

if api_key:
    url = f'http://www.omdbapi.com/?apikey={api_key}&t=Inception'
    print(f'Testing URL: {url}')
    
    response = requests.get(url)
    data = response.json()
    
    print(f'\nResponse: {data}')
    
    if data.get('Response') == 'True':
        print(f"\n✅ SUCCESS!")
        print(f"Title: {data.get('Title')}")
        print(f"Year: {data.get('Year')}")
        print(f"IMDB Rating: {data.get('imdbRating')}")
    else:
        print(f"\n❌ ERROR: {data.get('Error')}")
else:
    print('❌ No API key found!')
