# Self hosted AI interface

For this project we self-hosted an AI interface in our home server. 

## Hardware and Software data:

The AI interface is hosted in a virtual machine, on the server.
- 8 vCPU (virtual CPU)
- 8GB ram
- AMD Ryzen 5 7600 6-Core Processor

## Connection
Everyone can use the AI interface, if their computer is on our network (either by Wifi or VPN).

### VPN connection
The connection can be made with Wireguard software and a VPN configuriation.

#### Configuration data:

[Interface]

PrivateKey = *privatekey*

Address = *address*

[Peer]

PublicKey = *public key*

Endpoint = *endpoint*.org:4501

AllowedIPs = 192.168.*IP*/32

PersistentKeepalive = 25

## AI Interface

We selected and used the solution of Open WebUI.

https://openwebui.com/ 

From this website's documentation the self-hosting is reproduceable.


## Starting page
![image](https://github.com/user-attachments/assets/6386a886-2d3e-4cca-bbf6-1c4cd342d0d4)


## AI model

Open WebUI makes it possible to select any AI model from this website: https://ollama.com/library

![image](https://github.com/user-attachments/assets/f3210e6f-d658-4b6d-a06f-442f7b656313)

Just by searching for the AI model's name on the starting page, we can download and use the model.

![image](https://github.com/user-attachments/assets/aaf5fb66-b4f9-4160-a2eb-01bbe13dcf38)

After the : menas the LLM model's size. E.g: 10b means 10 billion.






