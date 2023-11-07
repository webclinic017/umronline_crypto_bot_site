import requests

url = "http://localhost:3100"

response = requests.post(url+"/tv_webbhook/gg", data="sell XRPUSDT")
print(response)

if response.status_code == 200:
    print('Alert request sent successfully!')
else:
    print(f'Alert request failed with status code: {response.status_code}')
    print('Response content:', response.content)