import webbrowser
import urllib.parse
api_key = "6775b45e-7648-4c89-a238-1351866d877a"
redirect_uri = "http://127.0.0.1:5800/vishal"
auth_url = f"https://api.upstox.com/v2/login/authorization/dialog?response_type=code&client_id={api_key}&redirect_uri={urllib.parse.quote(redirect_uri)}&state="

# Open the authorization URL in the browser
webbrowser.open(auth_url)

print("Please authorize the app and get the code from the redirect URL")

# import requests

# url = 'https://api.upstox.com/v2/login/authorization/token'
# headers = {
#     'accept': 'application/json',
#     'Content-Type': 'application/x-www-form-urlencoded',
# }

# api_key = "6775b45e-7648-4c89-a238-1351866d877a"
# api_secret = "1vit6q0lrk"
# redirect_uri = "http://127.0.0.1:5800/vishal"
# authorization_code = "lYTlwV"  # Replace with the actual code obtained

# data = {
#     'code': authorization_code,
#     'client_id': api_key,
#     'client_secret': api_secret,
#     'redirect_uri': redirect_uri,
#     'grant_type': 'authorization_code',
# }

# response = requests.post(url, headers=headers, data=data)

# print(response.status_code)
# print(response.json())
