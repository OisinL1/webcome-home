This project uses a raspberry pi to create a web app for the household.
This web app informs you who is at the house and the pi serves a livestream from the house at all times.

Features 
Lightweight Messaging: Streams video using HTTP for efficient delivery to web client
Network/API Programming: Flask provides a RESTful API to deliver the camera stream to browsers.
IoT Architecture: Bridges the Raspberry Pi camera with web browsers.
Home Presence Detection: Scans the local network for connected devices using Nmap and publishes device presence data to an MQTT broker.
Accessible: Ngrok is used for port forwarding, making the livestream available on the web app

Glitch URL (Ngrok account has exceeded bandwidth limit for the stream) - https://wood-fog-toad.glitch.me/
