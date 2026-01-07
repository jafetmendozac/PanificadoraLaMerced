import requests
from config import API_URL

def get(endpoint):
    return requests.get(f"{API_URL}{endpoint}")

def post(endpoint, data):
    return requests.post(f"{API_URL}{endpoint}", json=data)

def put(endpoint, data):
    return requests.put(f"{API_URL}{endpoint}", json=data)

def delete(endpoint):
    return requests.delete(f"{API_URL}{endpoint}")
