# SensoAguaV4Embedded
This proyect deploys a Bluetooth server within the Probetheus water quality probe's Raspberry Pi. The main functionalities are: 
* Being able to interact with the Probetheus mobile application in a two way protocol.
* Raw sensor data processing
* Probe state information
## Prerrequisites
1. Make sure your Raspberry Pi has Python 2.7.
## Instructions
1. Open the console, go inside the root folder and execute:
```bash
pip install -r requirements.txt
```
2. Configure the raspberry pi following the steps detailed in https://github.com/ole-vi/bluetooth-server, also configure the automated Bluetooth pairing optional part. Be sure to replace script route with the one that leads to **BTServer.py**.

3. Then execute the following commands in the terminal:
```bash
$ bluetoothctl 
$ discoverable on
$ pairable on
$ agent on
$ default-agent
$ exit
```

4. Last, delete the Bluetooth tool from de upper toolbar (this is going to allow us to connect to the probe without the manual verification)

</br></br>
**(NOTE)**: if you want to save as much power as possible, be sure that the WiFi is disabled.

