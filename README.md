# Gossip-based-human-tracking

Gossip-based-human-tracking uses OpenCV with raspberry pi cameras to track a person across a Pi-network using a Gossip-Protocol

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

You will need your raspberry pi's loaded up with 'Raspberry Pi OS with desktop' (since the lite version comes without all networking libraries).

Following these steps, should allow you to recreate the project:

```bash
sudo apt update
```
```bash
sudo apt install build-essential cmake
sudo apt install libgtk-3-dev
sudo apt install libboost-all-dev
```
```
pip3 install dlib
pip3 install skipy
pip3 install scikit-image
pip3 install face-recognition
```
It is recommended to work in a pyvenv, but if you prefer to work without one, add ``` --break-system-packages ``` at the end of the above pip commands
The installation needs to be done on all raspberry pi's that are supposed to be on the network.

Optionally, if you intend to use a raspberry pi without face-tracking, the default libraries that come with the 'Raspberry Pi Os with desktop' the standard libraries that come with the OS are enough.

## Usage

To add a person/face to the project, put a JPG of the person into the directory 'faces'. The name of the JPG is how the Person will be seen by the network. 
Example: A picture of Obama should be named "Obama.jpg".

To start the face-recognition with the gossip in your local network, run gossip.py with ```python3 gossip.py```
Note: Depending on your network and your submask, you might have to set your IP address and your subnet mask seperately (default is 192.168.2.x and 255.255.255.0)

To start the gossip without face-recognition, run gossip_no_facerec.py with ```python3 gossip_no_facerec.py```. This will broadcast the latest gossip in your network.
Additionally, if you wish for a nice representation of the latest gossip being sent around in your network, you can run display.py with ```python3 display.py```. 
There you can also assign different display colors to your pi's.

This project is designed such that it can be used with an Ad-hoc network, or your existing wifi-network at home. It should also work in a mesh-wifi network, but this has not been tested yet. 

### Ad-hoc network
To set up an Ad-hoc network, you need to follow these steps:
```bash
cd /etc/network
sudo cp interfaces wifi-interface
sudo nano adhoc-interface
```
Now copy the following and paste it into the file:
```bash
  auto lo
  iface lo inet loopback
  iface eth0 inet dhcp

  auto wlan0
  iface wlan0 inet static
  address 192.168.2.1
  netmask 255.255.255.0
  wireless-channel 4
  wireless-essid PiEyeNet
  wireless-mode ad-hoc
```
To enable the pi hosting the Ad-hoc network to assign an IP to the other raspberry pi's, execute following command
```bash
sudo apt-get install isc-dhcp-server
```
To configure the dhcp-server use:
```bash
sudo nano /etc/dhcp/dhcpd.conf
```
and change the contents to:
```bash
  ddns-update-style interim;
  default-lease-time 600;
  max-lease-time 7200;
  authoritative;
  log-facility local7;
  subnet 192.168.2.0 netmask 255.255.255.0 {
   range 192.168.2.5 192.168.2.150;

  }
```
With the ad-hoc network ready to go, switch to the network directory with
```bash
cd /etc/network
```
and enable it with:
```bash
sudo cp /etc/network/wifi-interface interfaces
```

Now you can connect all raspberry pi's to the network 'PiEyeNet' and start the gossip.py program.
