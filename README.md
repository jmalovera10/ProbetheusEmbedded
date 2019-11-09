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
2. Configure the raspberry pi following the steps detailed in https://github.com/ole-vi/bluetooth-server, also configure the automated Bluetooth pairing optional part. Be sure to replace script name with **BTServer.py**.</br></br>
**(NOTE)**: if the Raspberry Pi was configured correctly the next time you reboot, you will be able to connect to the Bluetooth server with your Probetheus mobile app. 

