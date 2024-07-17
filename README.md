# Gossip-based-human-tracking

Gossip-based-human-tracking uses OpenCV with raspberry pi cameras to track a person across a Pi-network using the Gossip-Protocol

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

You will need your raspberry pi's loaded up with Raspberry Pi OS with desktop (since the lite version comes without all networking libraries.

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
pip3 install skipüy
pip3 install scikit-image
pip3 install face-recognition
```
It is recommended to work in a pyvenv, but if you prefer to work without one, add ``` --break-system-packages ``` at the end of the above pip commands
