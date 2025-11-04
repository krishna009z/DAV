import requests

# Test the Flask API endpoint
url = 'http://127.0.0.1:5000/api/analyze/movie'
headers = {
    'Authorization': 'Bearer test-token',  # You'll need a real token
    'Content-Type': 'application/json'
}
data = {
    'movie_name': 'Inception'
}

print("Testing movie search endpoint...")
print(f"URL: {url}")
print(f"Data: {data}")

try:
    response = requests.post(url, json=data, headers=headers)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
