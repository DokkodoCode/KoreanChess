# KoreanChess
A simple implementation of Korean Chess

## Multiplayer

Currently, the multiplayer functionality is only useable with two computers within the same network.
It uses the private IP address of your computer, which only allows for connections between two computers on the same network. To get it to work you will need to use the public IP address of the host machine. I have tried using this method, but the school internet is probably getting in the way of using it.
You can get the public IP using this:
```
import requests

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip_info = response.json()
        return ip_info['ip']
    except requests.RequestException as e:
        print(f"Error retrieving IP: {e}")
        return None
```
